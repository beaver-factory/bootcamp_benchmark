from ..app import load_course_report_into_db
import pytest
import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

# print('here', os.environ.get("PSQL_CONNECTIONSTRING"))

# os.environ["PSQL_CONNECTIONSTRING"] = os.environ.get("PSQL_CONNECTIONSTRING")


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    conn = psycopg2.connect(os.environ.get("PSQL_DB_CREATION_STRING"))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute('DROP DATABASE IF EXISTS test_course_report;')
    cur.execute('CREATE DATABASE test_course_report;')

    conn.commit()
    cur.close()
    conn.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_dataframe():
    return pd.read_csv('./loader_course_report/__tests__/test_course_data.csv')


def test(create_test_dataframe):
    load_course_report_into_db(create_test_dataframe)
    assert 1 == 0
