import psycopg2
import os
import pandas as pd
import azure.functions as func
from io import BytesIO
import logging


def load_course_report_into_db(inBlob: func.InputStream):
    """
    Creates a connection to the PSQL server before creating course_report table and inserting data.

    """
    df = pd.read_csv(BytesIO(inBlob.read()))
    df.pop(df.columns[0])

    column_headers = ['provider_name', 'course_name', 'course_skills', 'course_locations', 'course_description', 'target_url', 'timestamp', 'course_country']

    handle_errors(column_headers, df)

    # establish connection to db, using env variable,
    # either ARM template connectionstring for production or .env for testing'
    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])
    logging.info('Successfully connected to PSQL server using PSQL_CONNECTIONSTRING to load course data')
    cur = conn.cursor()
    table_name = 'course_report'

    cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    cur.execute(f'''
            CREATE TABLE {table_name} (
                ID SERIAL PRIMARY KEY,
                provider_name VARCHAR(50),
                course_name VARCHAR(100),
                skill VARCHAR(50),
                course_location VARCHAR(50),
                description TEXT,
                collection_url TEXT,
                collection_date DATE,
                course_country VARCHAR(10)
            );
            ''')

    logging.info('Successfully created course_report table')

    tup = list(df.itertuples(index=False))

    # converting df rows into string for SQL query, while protecting from injection
    # enables multiple rows to be added to query string
    args_str = ','.join(cur.mogrify(
        "(%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in tup)

    cur.execute(f"""INSERT INTO {table_name} (
                 provider_name,
                 course_name,
                 skill,
                 course_location,
                 description,
                 collection_url,
                 collection_date,
                 course_country
             ) VALUES """ + args_str)

    logging.info('Successfully inserted values into course_report table')

    # !Important, make changes persist on db!
    conn.commit()

    # close it all down
    cur.close()
    conn.close()


def load_course_skills_into_db(inBlob: func.InputStream):
    """
    Creates a connection to the PSQL server before creating and course_skills table and inserting data.

    """
    df = pd.read_csv(BytesIO(inBlob.read()))
    df.pop(df.columns[0])

    column_headers = ['course_skills']

    handle_errors(column_headers, df)

    # establish connection to db, using env variable,
    # either ARM template connectionstring for production or .env for testing'
    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])
    logging.info('Successfully connected to PSQL server using PSQL_CONNECTIONSTRING to load skills data')

    cur = conn.cursor()
    table_name = 'course_skills'

    cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    cur.execute(f'''
            CREATE TABLE {table_name} (
                ID SERIAL PRIMARY KEY,
                skill VARCHAR(50)
            );
            ''')

    logging.info('Successfully created course_skills table')
    tup = list(df.itertuples(index=False))

    # converting df rows into string for SQL query, while protecting from injection
    # enables multiple rows to be added to query string
    args_str = ','.join(cur.mogrify("(%s)", x).decode('utf-8') for x in tup)

    cur.execute(f"""INSERT INTO {table_name} (skill) VALUES """ + args_str)

    logging.info('Successfully inserted values into course_skills table')

    # !Important, make changes persist on db!
    conn.commit()

    # close it all down
    cur.close()
    conn.close()


def handle_errors(column_headers, df):
    """Takes a list of headers and a dataframe, handles error checking by raising exceptions"""

    if df.columns.values.tolist() != column_headers:
        raise Exception('Invalid CSV column names')

    if len(df.index) == 0:
        raise Exception('CSV only has headers')

    if all(df.iloc[0].isnull().values.tolist()):
        raise Exception('CSV has headers but no data')
