import azure.functions as func
import pandas as pd
from .app import process_course_data, process_skills_data
import json
import logging


def main(inBlob: func.InputStream, outBlob: func.Out[bytes], outBlob2: func.Out[bytes], outBlob3: func.Out[bytes]):

    input_json = inBlob.read().decode('utf-8')

    if input_json == '' or input_json == '[]':
        raise Exception('Unprocessed json is empty, check json output from collector')

    input_obj = json.loads(input_json)

    locations = input_obj.pop(0)

    input = json.dumps(input_obj)
    input_df = pd.read_json(input)

    bootcamps_df = process_course_data(input_df, locations["uk_locations"])
    logging.info('Successfully processed course data')
    bootcamps_csv = bootcamps_df.to_csv()
    outBlob.set(bootcamps_csv.encode('utf-8'))

    skills_df = process_skills_data(input_df)
    logging.info('Successfully processed skills data')
    skills_csv = skills_df.to_csv()
    outBlob2.set(skills_csv.encode('utf-8'))
    outBlob3.set(skills_csv.encode('utf-8'))
