from ..app import load_course_report_into_db
import pytest
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from unittest.mock import patch, Mock
from dotenv import load_dotenv

load_dotenv()

# bug fix to prevent pytest from crashing
os.environ["no_proxy"] = "*"


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


def test_db_table_creation():
    new_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report.csv')
    load_course_report_into_db(new_inputstream)

    query = 'SELECT * FROM course_report;'
    results = db_results(query)

    assert len(results) > 0


def test_db_correct_lengths():
    new_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report.csv')
    load_course_report_into_db(new_inputstream)

    query = 'SELECT * FROM course_report;'
    results = db_results(query)

    assert len(results) == 10
    assert len(results[0]) == 10


def test_rows_are_different():
    new_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report.csv')
    load_course_report_into_db(new_inputstream)

    query = 'SELECT DISTINCT * FROM course_report;'
    results = db_results(query)
    print(results)

    assert len(results) == 10
    assert results[0] != results[1]


def test_throws_column_exception():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report_incorrect_col_name.csv')
        load_course_report_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'

    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report_missing_column.csv')
        load_course_report_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'


def test_csv_only_has_headers():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report_only_headers.csv')
        load_course_report_into_db(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'CSV only has headers'


def test_csv_has_headers_but_empty_rows():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report_headers_empty_rows.csv')
        load_course_report_into_db(new_inputstream)

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
