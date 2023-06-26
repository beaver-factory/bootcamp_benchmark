import pytest
import os
import json
from loader_utils import close_connection, generate_inputstream, establish_connection, generate_insertion_string
from ..app import load_course_skills_into_db
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import psycopg2
import pandas as pd

load_dotenv()

# bug fix to prevent pytest from crashing
os.environ["no_proxy"] = "*"

dirpath = 'loader_course_skills/__tests__/skills_dict.json'


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

    test_dict = {'Express': ['express', 'expressjs', 'express.js'], 'CSS': ['css', 'css3.0'], 'HTML': ['html', 'html5'], 'React': ['react', 'react.js', 'reactjs']}

    if os.path.isfile(dirpath):
        os.remove(dirpath)

    with open(f'{dirpath}', 'w') as file:
        file.write(json.dumps(test_dict))

    yield

    os.remove(dirpath)


def test_nothing():
    blob = generate_inputstream(dirpath)

    input_json = blob.read().decode('utf-8')

    df = pd.DataFrame([{"skills": skill} for skill in json.loads(input_json)])

    conn, cur = establish_connection()
    table_name = 'skills'

    cur.execute(f'''
                CREATE TABLE {table_name} (
                    ID SERIAL PRIMARY KEY,
                    skill VARCHAR(50)
                );
                ''')

    args_str = generate_insertion_string(df, cur, 1)

    cur.execute(f"""INSERT INTO {table_name} (skill) VALUES """ + args_str)

    close_connection(cur, conn)

    load_course_skills_into_db(blob)
    assert 1 == 0
