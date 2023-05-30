import psycopg2
import os


def load_course_report_into_db(input_df):
    # establish connection to db, using ARM template connectionstring'
    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])
    cur = conn.cursor()
    # only drop and insert if new csv contains some data

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
                collection_url TEXT,
                collection_date TEXT
            );
            ''')

    input_df.pop(input_df.columns[0])
    # tup = input_df.apply(tuple, axis=1).tolist()
    tup = list(input_df.itertuples(index=False))

    args_str = ','.join(cur.mogrify(
        "(%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in tup)

    cur.execute("""INSERT INTO course_report (
                 provider_name,
                 track,
                 course_name,
                 skill,
                 course_location,
                 description,
                 collection_url,
                 collection_date
             ) VALUES """ + args_str)

    # !Important, make changes persist on db!
    conn.commit()

    # close it all down
    cur.close()
    conn.close()
