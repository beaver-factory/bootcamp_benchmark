import pandas as pd
from azure.functions import InputStream
from io import BytesIO
import logging
from utils import handle_loader_errors, establish_connection, close_connection, generate_insertion_string


def load_course_report_into_db(inBlob: InputStream):
    """
    Creates a connection to the PSQL server before creating course_report table and inserting data.

    """
    df = pd.read_csv(BytesIO(inBlob.read()))
    df.pop(df.columns[0])

    column_headers = ['provider_name', 'course_name', 'course_skills', 'course_locations', 'course_description', 'target_url', 'timestamp', 'course_country']

    handle_loader_errors(column_headers, df)

    conn, cur = establish_connection()
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

    logging.info(f'Successfully created {table_name} table')

    args_str = generate_insertion_string(df, cur, 8)

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

    logging.info(f'Successfully inserted values into {table_name} table')

    close_connection(cur, conn)


def load_course_skills_into_db(inBlob: func.InputStream):
    """
    Creates a connection to the PSQL server before creating and course_skills table and inserting data.

    """
    df = pd.read_csv(BytesIO(inBlob.read()))
    df.pop(df.columns[0])

    column_headers = ['course_skills']
    handle_loader_errors(column_headers, df)

    conn, cur = establish_connection()
    table_name = 'course_skills'

    cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    cur.execute(f'''
            CREATE TABLE {table_name} (
                ID SERIAL PRIMARY KEY,
                skill VARCHAR(50)
            );
            ''')

    logging.info(f'Successfully created {table_name} table')

    args_str = generate_insertion_string(df, cur, 1)

    cur.execute(f"""INSERT INTO {table_name} (skill) VALUES """ + args_str)

    logging.info(f'Successfully inserted values into {table_name} table')

    close_connection(cur, conn)
