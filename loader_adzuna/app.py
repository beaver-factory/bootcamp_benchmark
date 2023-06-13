import pandas as pd
import azure.functions as func
from io import BytesIO
import logging
from utils import handle_loader_errors, establish_connection, close_connection, generate_insertion_string


def load_adzuna_jobs_per_skill(inBlob: func.InputStream):
    """
    Creates a connection to the PSQL server before creating adzuna_job_counts table and inserting data.

    """
    df = pd.read_csv(BytesIO(inBlob.read()))

    column_headers = ['skill', 'number_of_jobs']

    handle_loader_errors(column_headers, df)

    conn, cur = establish_connection()
    table_name = 'adzuna_job_counts'

    cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    cur.execute(f'''
            CREATE TABLE {table_name} (
                ID SERIAL PRIMARY KEY,
                skill VARCHAR(50),
                job_count INT
            );
            ''')

    logging.info(f'Successfully created {table_name} table')

    # converting df rows into string for SQL query, while protecting from injection
    # enables multiple rows to be added to query string
    args_str = generate_insertion_string(df, cur, 2)

    cur.execute(f"""INSERT INTO {table_name} (
                 skill,
                 job_count
             ) VALUES """ + args_str)

    logging.info(f'Successfully inserted values into {table_name} table')

    close_connection(cur, conn)
