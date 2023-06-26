import pandas as pd
from azure.functions import InputStream
from io import BytesIO
import logging
from loader_utils import db_results, establish_connection, close_connection, generate_insertion_string
import json


def load_course_skills_into_db(inBlob: InputStream):
    """
    Connects to the PSQL server, creates course_skills table, inserts data.

        :param inBlob: Azure input stream from blob trigger
        :type inBlob: InputStream
    """

    input_json = inBlob.read().decode('utf-8')

    df = pd.DataFrame([{"skills": skill} for skill in json.loads(input_json)])
    # df.pop(df.columns[0])

    conn, cur = establish_connection()
    table_name = 'skills'

    # cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (table_name,))

    if not cur.fetchone()[0]:
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
    else:
        conn, cur = establish_connection()

        sel_skills = f'SELECT * FROM {table_name};'
        skills = db_results(sel_skills)
        existing_skills = pd.DataFrame(skills)
        existing_skills.pop(existing_skills.columns[0])

        print(existing_skills)

        # args_str = generate_insertion_string(df, cur, 1)

        # cur.execute(f"""INSERT INTO {table_name} (skill) VALUES """ + args_str)

        # logging.info(f'Successfully inserted values into {table_name} table')

        close_connection(cur, conn)
