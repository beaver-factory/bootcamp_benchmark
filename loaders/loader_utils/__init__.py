import psycopg2.extensions
import logging
import os
from typing import Tuple, List
from pandas import DataFrame
from unittest.mock import patch, Mock
from dotenv import load_dotenv


def handle_loader_errors(column_headers: List[str], df: DataFrame):
    """Common Error handling for loader functions

    :param column_headers: a whitelist of column headers
    :type column_headers: List[str]
    :param df: the dataframe containing values to check
    :type df: DataFrame
    :raises Exception: CSV column name error
    :raises Exception: CSV lacking data
    :raises Exception: CSV empty rows
    """

    if df.columns.values.tolist() != column_headers:
        raise Exception('Invalid CSV column names')

    if len(df.index) == 0:
        raise Exception('CSV only has headers')

    if all(df.iloc[0].isnull().values.tolist()):
        raise Exception('CSV has headers but no data')


def establish_connection() -> Tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
    """Establishes a psycopg2 connection using env variable

    :return: the connection and cursor
    :rtype: Tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]
    """

    # either ARM template connectionstring for production or .env for testing'
    load_dotenv()

    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])

    cur = conn.cursor()

    logging.info(
        'Successfully connected to PSQL server using PSQL_CONNECTIONSTRING to load course data')

    return conn, cur


def close_connection(cur: psycopg2.extensions.cursor, conn: psycopg2.extensions.connection):
    """Commits then Closes a given psycopg2 connection and cursor

    :param cur: psycopg2 cursor
    :type cur: psycopg2.extensions.cursor
    :param conn: psycopg2 connection
    :type conn: psycopg2.extensions.connection
    """

    # !Important, make changes persist on db!
    conn.commit()

    # close it all down
    cur.close()
    conn.close()


def generate_insertion_string(df: DataFrame, cur: psycopg2.extensions.cursor, col_quant: int) -> str:
    """Generates a valid table insertion string for use in a PSQL query with multiple rows

    :param df: pandas dataframe
    :type df: DataFrame
    :param cur: psycopg2 cursor
    :type cur: psycopg2.extensions.cursor
    :param col_quant: number representing the number of columns
    :type col_quant: int
    :return: string for use in a PSQL query
    :rtype: str
    """
    tup = list(df.itertuples(index=False))

    # arrange string in format (%s,%s,%s...)
    string_with_insertions = "(" + ("%s," * col_quant)
    finalised_string = string_with_insertions[:-1] + ")"

    return ','.join(cur.mogrify(finalised_string, x).decode('utf-8') for x in tup)


def db_results(query: str):
    """Executes a query on the containerised test db

    :param query: query to execute on the db
    :type query: str
    :return: _description_
    :rtype: list[tuple(any)]
    """

    conn, cur = establish_connection()

    cur.execute(query)
    rows = cur.fetchall()

    close_connection(cur, conn)

    return rows


def generate_inputstream(path: str):
    """Converts a local csv file to a mock azure inputstream format

    :param path: path of a local csv file
    :type path: str
    :return: a mocked azure blob input stream containing the csv data
    :rtype: InputStream
    """

    with open(path, 'rb') as file:
        test_csv_data = file.read()

    mock_inputstream = Mock()
    mock_inputstream.read.return_value = test_csv_data

    with patch('azure.functions.InputStream', return_value=mock_inputstream):
        return mock_inputstream
