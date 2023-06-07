from ..app import load_course_report_into_db, load_course_skills_into_db
import pytest
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from unittest.mock import patch, Mock
from dotenv import load_dotenv
import pandas as pd
import shutil

load_dotenv()

# bug fix to prevent pytest from crashing
os.environ["no_proxy"] = "*"
dirpath = 'loader_course_report/__tests__/csv'


@pytest.fixture(scope="session", autouse=True)
def create_csv():

    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

    column_headers = ['provider_name', 'course_name', 'course_skills', 'course_locations', 'course_description', 'target_url', 'timestamp', 'course_country']
    skills_header = ['course_skills']

    generate_csv(column_headers)
    generate_skills_csvs(skills_header)

    yield

    shutil.rmtree(dirpath)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """connects to docker containerised psql server and created test db"""
    conn = psycopg2.connect("host='localhost' user='db_admin' password='password123'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute('DROP DATABASE IF EXISTS test_course_report;')
    cur.execute('CREATE DATABASE test_course_report;')

    conn.commit()
    cur.close()
    conn.close()


# course_report

def test_db_table_creation():
    new_inputstream = generate_inputstream(f'{dirpath}/test_course_report.csv')
    load_course_report_into_db(new_inputstream)

    query = 'SELECT * FROM course_report;'
    results = db_results(query)

    assert len(results) > 0


def test_db_correct_lengths():
    new_inputstream = generate_inputstream(f'{dirpath}/test_course_report.csv')
    load_course_report_into_db(new_inputstream)

    query = 'SELECT * FROM course_report;'
    results = db_results(query)

    assert len(results) == 3
    assert len(results[0]) == 9


def test_rows_are_different():
    new_inputstream = generate_inputstream(f'{dirpath}/test_course_report.csv')
    load_course_report_into_db(new_inputstream)

    query = 'SELECT DISTINCT * FROM course_report;'
    results = db_results(query)

    assert len(results) == 3
    assert results[0] != results[1]


def test_throws_column_exception():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_course_report_incorrect_col_name.csv')
        load_course_report_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'

    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_course_report_missing_column.csv')
        load_course_report_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'


def test_csv_only_has_headers():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_course_report_only_headers.csv')
        load_course_report_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'CSV only has headers'


def test_csv_has_headers_but_empty_rows():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_course_report_headers_empty_rows.csv')
        load_course_report_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'CSV has headers but no data'


# course_skills

def test_skills_table_creation():
    new_inputstream = generate_inputstream(f'{dirpath}/test_course_skills.csv')
    load_course_skills_into_db(new_inputstream)

    query = 'SELECT * FROM course_skills;'
    results = db_results(query)

    assert len(results) > 0


def test_skills_correct_lengths():
    new_inputstream = generate_inputstream(f'{dirpath}/test_course_skills.csv')
    load_course_skills_into_db(new_inputstream)

    query = 'SELECT * FROM course_skills;'
    results = db_results(query)

    assert len(results) == 3
    assert len(results[0]) == 2


def test_rows_are_unique():
    new_inputstream = generate_inputstream(f'{dirpath}/test_course_skills.csv')
    load_course_skills_into_db(new_inputstream)

    query = 'SELECT DISTINCT * FROM course_skills;'
    results = db_results(query)
    values = [x[1] for x in results]

    query2 = 'SELECT * FROM course_skills;'
    results2 = db_results(query2)
    values2 = [x[1] for x in results2]

    assert all(item in values2 for item in values)


def test_skills_throws_column_exception():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_course_skills_incorrect_col_name.csv')
        load_course_skills_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'

    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_course_skills_missing_column.csv')
        load_course_skills_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'


def test_skills_csv_only_has_headers():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_course_skills_only_headers.csv')
        load_course_skills_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'CSV only has headers'


def test_skills_csv_has_headers_but_empty_rows():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_course_skills_headers_empty_rows.csv')
        load_course_skills_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'CSV has headers but no data'


# helpers

def generate_inputstream(path):
    """converts a local csv file and returns a mocked blob input stream containing that data"""
    with open(path, 'rb') as file:
        test_csv_data = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_csv_data

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream


def db_results(query):
    """takes an SQL query and returns a list of all rows (as tuples) from the containerised test db"""
    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])
    cur = conn.cursor()

    cur.execute(query)
    rows = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return rows


def generate_csv(headers):
    """takes a list of headers and outputs a base csv and test csv's"""

    os.mkdir(f'{dirpath}')
    df = pd.DataFrame(columns=headers)

    # headers only csv
    df.to_csv(f'{dirpath}/test_course_report_only_headers.csv')

    # empty rows
    df.loc[0] = ["" for header in headers]

    df.to_csv(f'{dirpath}/test_course_report_headers_empty_rows.csv')

    # base csv
    for i in range(3):
        df.loc[i] = ['test' for header in headers]

    df['timestamp'] = df['timestamp'].replace('test', '2023-01-01')
    df.to_csv(f'{dirpath}/test_course_report.csv')

    # incorrect col names
    df.rename(columns={'course_name': 'name'}, inplace=True)

    df.to_csv(f'{dirpath}/test_course_report_incorrect_col_name.csv')

    # missing col
    df = df.drop(columns=['name'])

    df.to_csv(f'{dirpath}/test_course_report_missing_column.csv')


def generate_skills_csvs(headers):
    """takes a list of headers and outputs a base csv and test csv's"""

    df = pd.DataFrame(columns=headers)

    # headers only csv
    df.to_csv(f'{dirpath}/test_course_skills_only_headers.csv')

    # empty rows
    df.loc[0] = ["" for header in headers]

    df.to_csv(f'{dirpath}/test_course_skills_headers_empty_rows.csv')

    # base csv
    for i in range(3):
        df.loc[i] = [f'test{i}' for header in headers]

    df.to_csv(f'{dirpath}/test_course_skills.csv')

    # incorrect col names
    df.rename(columns={'course_skills': 'skill'}, inplace=True)

    df.to_csv(f'{dirpath}/test_course_skills_incorrect_col_name.csv')

    # missing col
    df = df.drop(columns=['skill'])

    df.to_csv(f'{dirpath}/test_course_skills_missing_column.csv')
