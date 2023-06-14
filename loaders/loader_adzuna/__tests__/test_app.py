from ..app import load_adzuna_jobs_per_skill
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

# globals

dirpath = 'loaders/loader_adzuna/__tests__/csv'

# fixtures


@pytest.fixture(scope="session", autouse=True)
def create_csv():

    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

    column_headers = ['skill', 'number_of_jobs']

    generate_csv(column_headers)

    yield

    shutil.rmtree(dirpath)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """connects to docker containerised psql server and created test db"""
    conn = psycopg2.connect("host='localhost' user='db_admin' password='password123'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute('DROP DATABASE IF EXISTS test_db;')
    cur.execute('CREATE DATABASE test_db;')

    conn.commit()
    cur.close()
    conn.close()

# tests


def test_db_table_creation():
    new_inputstream = generate_inputstream(f'{dirpath}/test_adzuna.csv')
    load_adzuna_jobs_per_skill(new_inputstream)

    query = 'SELECT * FROM adzuna_job_counts;'
    results = db_results(query)

    assert len(results) > 0


def test_db_correct_lengths():
    new_inputstream = generate_inputstream(f'{dirpath}/test_adzuna.csv')
    load_adzuna_jobs_per_skill(new_inputstream)

    query = 'SELECT * FROM adzuna_job_counts;'
    results = db_results(query)

    assert len(results) == 3
    assert len(results[0]) == 3


def test_rows_are_different():
    new_inputstream = generate_inputstream(f'{dirpath}/test_adzuna.csv')
    load_adzuna_jobs_per_skill(new_inputstream)

    query = 'SELECT * FROM adzuna_job_counts;'
    results = db_results(query)

    assert len(results) == 3
    assert results[0] != results[1]


def test_rows_are_unique():
    new_inputstream = generate_inputstream(f'{dirpath}/test_adzuna.csv')
    load_adzuna_jobs_per_skill(new_inputstream)

    query = 'SELECT DISTINCT * FROM adzuna_job_counts;'
    results = db_results(query)
    values = [x[1] for x in results]

    query2 = 'SELECT * FROM adzuna_job_counts;'
    results2 = db_results(query2)
    values2 = [x[1] for x in results2]

    assert all(item in values2 for item in values)


def test_throws_column_exception():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_adzuna_incorrect_col_name.csv')
        load_adzuna_jobs_per_skill(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'

    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_adzuna_missing_column.csv')
        load_adzuna_jobs_per_skill(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'Invalid CSV column names'


def test_csv_only_has_headers():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_adzuna_only_headers.csv')
        load_adzuna_jobs_per_skill(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'CSV only has headers'


def test_csv_has_headers_but_empty_rows():
    with pytest.raises(Exception) as csv_error:
        new_inputstream = generate_inputstream(f'{dirpath}/test_adzuna_headers_empty_rows.csv')
        load_adzuna_jobs_per_skill(new_inputstream)

    print(f'Error is: {str(csv_error.value)}')
    assert str(csv_error.value) == 'CSV has headers but no data'
# helpers


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


def generate_inputstream(path):
    """converts a local csv file and returns a mocked blob input stream containing that data"""
    with open(path, 'rb') as file:
        test_csv_data = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_csv_data

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream


def generate_csv(headers):
    """takes a list of headers and outputs a base csv and test csv's"""

    os.mkdir(f'{dirpath}')
    df = pd.DataFrame(columns=headers)

    # headers only csv
    df.to_csv(f'{dirpath}/test_adzuna_only_headers.csv', index=False)

    # empty rows
    df.loc[0] = ["" for header in headers]

    df.to_csv(f'{dirpath}/test_adzuna_headers_empty_rows.csv', index=False)

    # base csv
    for i in range(3):
        df.loc[i] = [f'test{i}', i]

    df.to_csv(f'{dirpath}/test_adzuna.csv', index=False)

    # incorrect col names
    df.rename(columns={headers[0]: 'diplodocus'}, inplace=True)

    df.to_csv(f'{dirpath}/test_adzuna_incorrect_col_name.csv', index=False)

    # missing col
    df = df.drop(columns=['diplodocus'])

    df.to_csv(f'{dirpath}/test_adzuna_missing_column.csv', index=False)
