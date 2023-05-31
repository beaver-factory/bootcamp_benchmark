from ..app import load_course_report_into_db
import pytest
import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from unittest.mock import patch, Mock
from io import BytesIO

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    # connect to docker containerised psql server
    conn = psycopg2.connect("host='localhost' user='db_admin' password='password123'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute('DROP DATABASE IF EXISTS test_course_report;')
    cur.execute('CREATE DATABASE test_course_report;')

    conn.commit()
    cur.close()
    conn.close()


def generate_inputstream(path):
    with open(path, 'rb') as file:
        test_csv_data = BytesIO(file.read())

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_csv_data

    return mock_inputstream


@pytest.fixture
def mock_blob_inputstream_correct_data():
    mock_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report.csv')

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        yield mock_inputstream


@pytest.fixture
def mock_blob_inputstream_incorrect_col_name():
    mock_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report_incorrect_col_name.csv')

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        yield mock_inputstream


@pytest.fixture
def mock_blob_inputstream_missing_column():
    mock_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report_missing_column.csv')

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        yield mock_inputstream


@pytest.fixture
def mock_blob_inputstream_empty():
    mock_inputstream = generate_inputstream('./loader_course_report/__tests__/test_course_report_only_headers.csv')

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        yield mock_inputstream


def test_db_table_creation(mock_blob_inputstream_correct_data):

    load_course_report_into_db(mock_blob_inputstream_correct_data)

    query = 'SELECT * FROM course_report;'
    results = db_results(query)

    assert len(results) != 0


def test_db_correct_lengths(mock_blob_inputstream_correct_data):

    load_course_report_into_db(mock_blob_inputstream_correct_data)

    query = 'SELECT * FROM course_report;'
    results = db_results(query)

    assert len(results) == 10
    assert len(results[0]) == 9


def test_rows_are_different(mock_blob_inputstream_correct_data):
    load_course_report_into_db(mock_blob_inputstream_correct_data)

    query = 'SELECT DISTINCT * FROM course_report;'
    results = db_results(query)

    assert len(results) == 10
    assert results[0] != results[1]


def test_throws_column_exception(mock_blob_inputstream_incorrect_col_name, mock_blob_inputstream_missing_column):
    with pytest.raises(Exception) as csv_error:
        load_course_report_into_db(mock_blob_inputstream_incorrect_col_name)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'

    with pytest.raises(Exception) as csv_error:
        load_course_report_into_db(mock_blob_inputstream_missing_column)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'


def test_empty_blob(mock_blob_inputstream_empty):
    with pytest.raises(Exception) as csv_error:
        load_course_report_into_db(mock_blob_inputstream_empty)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'CSV is empty'


# helpers
def db_results(query):
    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])
    cur = conn.cursor()

    cur.execute(query)
    rows = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return rows
