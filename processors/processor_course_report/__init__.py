from azure.functions import InputStream, Out
import pandas as pd
from .app import process_course_data, process_skills_data
import json
import logging


def main(inBlob: InputStream, inBlob2: InputStream, outBlob: Out[bytes], outBlob2: Out[bytes], outBlob3: Out[bytes], outBlob4: Out[bytes]):
    """Main function for processor_course_report

    :param inBlob: Azure input blob
    :type inBlob: InputStream
    :param inBlob2: Azure input blob
    :type inBlob2: InputStream
    :param outBlob: Azure output blob
    :type outBlob: Out[bytes]
    :param outBlob2: Azure output blob
    :type outBlob2: Out[bytes]
    :param outBlob3: Azure output blob
    :type outBlob3: Out[bytes]
    :param outBlob4: Azure output blob
    :type outBlob4: Out[bytes]
    :raises Exception: Empty blob alert
    :raises Exception: Json empty alert
    """
    input_json = inBlob.read().decode('utf-8')

    if input_json == '':
        raise Exception('Blob is empty, check json output from collector')

    input_obj = json.loads(input_json)

    if len(input_obj) == 0:
        raise Exception('Unprocessed json is empty, check json output from collector')

    locations = input_obj.pop(0)

    input = json.dumps(input_obj)
    input_df = pd.read_json(input)

    bootcamps_df = process_course_data(input_df, locations["uk_locations"], inBlob2, outBlob4)
    logging.info('Successfully processed course data')
    bootcamps_csv = bootcamps_df.to_csv()
    outBlob.set(bootcamps_csv.encode('utf-8'))

    skills_df = process_skills_data(bootcamps_df)
    logging.info('Successfully processed skills data')
    skills_csv = skills_df.to_csv()
    outBlob2.set(skills_csv.encode('utf-8'))
    outBlob3.set(skills_csv.encode('utf-8'))
