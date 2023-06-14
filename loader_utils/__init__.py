import psycopg2.extensions
import logging
import os
from typing import Tuple, List
from pandas import DataFrame


def handle_loader_errors(column_headers: List[str], df: DataFrame):
    """Takes a list of headers and a dataframe, handles error checking by raising exceptions"""

    if df.columns.values.tolist() != column_headers:
        raise Exception('Invalid CSV column names')

    if len(df.index) == 0:
        raise Exception('CSV only has headers')

    if all(df.iloc[0].isnull().values.tolist()):
        raise Exception('CSV has headers but no data')


def establish_connection() -> Tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
    """Establishes a psycopg2 connection using env variable, creates a cursor and returns the connection and cursor"""
    # either ARM template connectionstring for production or .env for testing'
    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])

    cur = conn.cursor()

    logging.info('Successfully connected to PSQL server using PSQL_CONNECTIONSTRING to load course data')

    return conn, cur


def close_connection(cur: psycopg2.extensions.cursor, conn: psycopg2.extensions.connection):
    """Commits then Closes a given psycopg2 connection and cursor"""

    # !Important, make changes persist on db!
    conn.commit()

    # close it all down
    cur.close()
    conn.close()


def generate_insertion_string(df: DataFrame, cur: psycopg2.extensions.cursor, col_quant: int) -> str:
    """Takes a pandas dataframe, a psycopg2 cursor and a number representing the number of columns. Generates a valid table insertion string for use in a PSQL query with multiple rows"""

    tup = list(df.itertuples(index=False))

    # arrange string in format (%s,%s,%s...)
    string_with_insertions = "(" + ("%s," * row_quant)
    finalised_string = string_with_insertions[:-1] + ")"

    return ','.join(cur.mogrify(finalised_string, x).decode('utf-8') for x in tup)
