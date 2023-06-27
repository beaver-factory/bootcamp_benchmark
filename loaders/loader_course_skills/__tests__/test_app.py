import pytest
import os
import json
from loader_utils import close_connection, generate_inputstream, establish_connection, generate_insertion_string, db_results
from ..app import load_course_skills_into_db
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import psycopg2
import pandas as pd

load_dotenv()

# bug fix to prevent pytest from crashing
os.environ["no_proxy"] = "*"

dirpath = 'loader_course_skills/__tests__/skills_dict.json'
dirpath2 = 'loader_course_skills/__tests__/skills_dict2.json'


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Connects to docker containerised psql server and creates test db"""

    conn = psycopg2.connect(
        "host='localhost' user='db_admin' password='password123'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute('DROP DATABASE IF EXISTS test_db;')
    cur.execute('CREATE DATABASE test_db;')

    close_connection(cur, conn)


@pytest.fixture(scope="session", autouse=True)
def create_json():
    """Checks if test jsons are created, deletes if so, then generates fresh ones"""

    test_dict = {'Express': ['express', 'expressjs', 'express.js'], 'CSS': ['css', 'css3.0'], 'HTML': ['html', 'html5'], 'React': ['react', 'react.js', 'reactjs'], 'Angular': ['angular']}

    if os.path.isfile(dirpath):
        os.remove(dirpath)

    with open(f'{dirpath}', 'w') as file:
        file.write(json.dumps(test_dict))

    test_dict2 = {'Express': ['express', 'expressjs', 'express.js'], 'CSS': ['css', 'css3.0'], 'HTML': ['html', 'html5'], 'React': ['react', 'react.js', 'reactjs'], 'Angular': ['angular'], "Vue": ["vue", "vue.js"]}

    if os.path.isfile(dirpath2):
        os.remove(dirpath2)

    with open(f'{dirpath2}', 'w') as file2:
        file2.write(json.dumps(test_dict2))

    yield

    os.remove(dirpath)
    os.remove(dirpath2)


def create_table():
    """Creates a table for use in testing"""

    conn, cur = establish_connection()
    table_name = 'skills'
    df = pd.DataFrame([{"skills": "Angular"}])

    cur.execute(f'DROP TABLE IF EXISTS {table_name};')
    cur.execute(f'''
                CREATE TABLE {table_name} (
                    ID SERIAL PRIMARY KEY,
                    skill VARCHAR(50)
                );
                ''')

    args_str = generate_insertion_string(df, cur, 1)

    cur.execute(f"""INSERT INTO {table_name} (skill) VALUES """ + args_str)

    close_connection(cur, conn)


def test_skills_table_exists():
    create_table()

    result = db_results("select exists(select * from information_schema.tables where table_name='skills')")

    assert result[0][0]


def test_creates_skills_table_and_inserts_skills_when_table_does_not_exist():
    blob = generate_inputstream(dirpath)

    load_course_skills_into_db(blob)

    result_check_table = db_results("select exists(select * from information_schema.tables where table_name='skills')")
    result_check_skills = db_results("select * from skills")

    skills_to_check = [x[1] for x in result_check_skills]

    expected_skills = ['Angular', 'Express', 'CSS', 'HTML', 'React']

    assert result_check_table[0][0]

    assert len(skills_to_check) == 5
    assert all(element in skills_to_check for element in expected_skills)


def test_inserts_new_skill():
    create_table()
    blob = generate_inputstream(dirpath2)

    load_course_skills_into_db(blob)

    result = db_results('select * from skills')

    assert len(result) == 6


def test_does_not_add_duplicates():
    create_table()
    blob = generate_inputstream(dirpath)

    load_course_skills_into_db(blob)
    load_course_skills_into_db(blob)

    result = db_results('select * from skills')

    assert len(result) == 5


def test_rows_are_unique():
    create_table()
    blob = generate_inputstream(dirpath)

    load_course_skills_into_db(blob)

    results = db_results('select distinct * from skills;')
    values = [x[1] for x in results]

    results2 = db_results('select * from skills;')
    values2 = [x[1] for x in results2]

    assert all(item in values2 for item in values)
