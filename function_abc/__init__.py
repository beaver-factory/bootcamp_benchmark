import azure.functions as func
import json
import os
import psycopg2

def main(inBlob: func.InputStream):
    # read data from blob and update string
    jsonData = json.loads(inBlob.read())
    ab_string = jsonData['value']
    abc_string = ab_string + 'c'

    # establish connection to db, using ARM template connectionstring'
    conn = psycopg2.connect(os.environ["PSQL_CONNECTIONSTRING"])
    cur = conn.cursor()

    # create and insert data into table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS abc (
            ID SERIAL PRIMARY KEY,
            abc_string VARCHAR(50)
        );
        '''
    )

    cur.execute("INSERT INTO abc (abc_string) VALUES (%s);", (abc_string,))

    # !Important, make changes persist on db!
    conn.commit()

    # close it all down
    cur.close()
    conn.close()

