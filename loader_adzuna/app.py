import pandas as pd
import azure.functions as func
import psycopg2
import os
from io import BytesIO
import logging


def load_adzuna_jobs_per_skill(inBlob: func.InputStream):
    """
    Creates a connection to the PSQL server before creating adzuna_job_counts table and inserting data.

    """
    df = pd.read_csv(BytesIO(inBlob.read()))

    column_headers = ['skill', 'number_of_jobs']

    handle_errors(column_headers, df)

    # establish connection to db, using env variable,
    # either ARM template connectionstring for production or .env for testing'
    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])
    logging.info('Successfully connected to PSQL server using PSQL_CONNECTIONSTRING to load Adzuna jobs data')
    cur = conn.cursor()
    table_name = 'adzuna_job_counts'

    cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    cur.execute(f'''
            CREATE TABLE {table_name} (
                ID SERIAL PRIMARY KEY,
                skill VARCHAR(50),
                job_count INT
            );
            ''')

    logging.info('Successfully created adzuna_job_counts table')

    tup = list(df.itertuples(index=False))

    # converting df rows into string for SQL query, while protecting from injection
    # enables multiple rows to be added to query string
    args_str = ','.join(cur.mogrify(
        "(%s,%s)", x).decode('utf-8') for x in tup)

    cur.execute(f"""INSERT INTO {table_name} (
                 skill,
                 job_count
             ) VALUES """ + args_str)

    logging.info('Successfully inserted values into adzuna_job_counts table')

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
