import azure.functions as func
import pandas as pd
from .app import process_scraped_data, process_skills_data
import json


def main(inBlob: func.InputStream, outBlob: func.Out[bytes], outBlob2: func.Out[bytes]):

    input_json = inBlob.read().decode('utf-8')
    input_obj = json.loads(input_json)

    locations = input_obj.pop(0)

    input = json.dumps(input_obj)
    input_df = pd.read_json(input)

    bootcamps_df = process_scraped_data(input_df, locations["uk_locations"])
    bootcamps_csv = bootcamps_df.to_csv()
    outBlob.set(bootcamps_csv.encode('utf-8'))

    skills_df = process_skills_data(input_df)
    skills_csv = skills_df.to_csv()
    outBlob2.set(skills_csv.encode('utf-8'))
