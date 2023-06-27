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

    conn, cur = establish_connection()
    table_name = 'skills'

    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (table_name,))

    if not cur.fetchone()[0]:
        df = pd.DataFrame([{"skills": skill} for skill in json.loads(input_json)])
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

        existing_skills = []

        for tup in skills:
            existing_skills.append(tup[1])

        new_skills = list(json.loads(input_json).keys())

        skills_to_add = []

        for skill in new_skills:
            if skill not in existing_skills:
                skills_to_add.append(skill)

        if len(skills_to_add) > 0:

            new_skills_df = pd.DataFrame([{"skills": skill} for skill in skills_to_add])

            args_str = generate_insertion_string(new_skills_df, cur, 1)

            cur.execute(f"""INSERT INTO {table_name} (skill) VALUES """ + args_str)

            logging.info(f'Successfully inserted values into {table_name} table')

        close_connection(cur, conn)
