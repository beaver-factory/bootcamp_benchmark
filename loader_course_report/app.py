import psycopg2
import os
import pandas as pd
import azure.functions as func


def load_course_report_into_db(inBlob: func.InputStream):
    df = pd.read_csv(inBlob.read())
    df.pop(df.columns[0])

    column_headers = ['provider_name', 'provider_tracks', 'course_name', 'course_skills', 'course_locations', 'course_description', 'time', 'target_url', 'timestamp']

    if df.columns.values.tolist() != column_headers:
        raise Exception('Invalid CSV column names')

    if len(df.index) == 0:
        raise Exception('CSV only has headers')

    if all(df.iloc[0].isnull().values.tolist()):
        raise Exception('CSV has headers but no data')

    # establish connection to db, using ARM template connectionstring'
    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])
    cur = conn.cursor()

    # do we want to drop table or keep a record of previous scraped data? What if all data is dropped?
    cur.execute('DROP TABLE IF EXISTS course_report')

    cur.execute('''
            CREATE TABLE course_report (
                ID SERIAL PRIMARY KEY,
                provider_name VARCHAR(50),
                track VARCHAR(50),
                course_name VARCHAR(100),
                skill VARCHAR(50),
                course_location TEXT,
                description TEXT,
                time_commitment VARCHAR(20),
                collection_url TEXT,
                collection_date DATE
            );
            ''')

    tup = list(df.itertuples(index=False))

    args_str = ','.join(cur.mogrify(
        "(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in tup)

    cur.execute("""INSERT INTO course_report (
                 provider_name,
                 track,
                 course_name,
                 skill,
                 course_location,
                 description,
                 time_commitment,
                 collection_url,
                 collection_date
             ) VALUES """ + args_str)

    # !Important, make changes persist on db!
    conn.commit()

    # close it all down
    cur.close()
    conn.close()
