from azure.functions import InputStream, Out
import pandas as pd
from .app import process_course_data, process_skills_data
import json
import logging


def main(inCourseReport: InputStream, inSkillsDict: InputStream, outCourseReport: Out[bytes], outHistoricSkills: Out[bytes], outLatestSkills: Out[bytes], outSkillsDict: Out[bytes]):
    """Main function for processor_course_report

    :param inCourseReport: Azure input blob
    :type inCourseReport: InputStream
    :param inSkillsDict: Azure input blob
    :type inSkillsDict: InputStream
    :param outCourseReport: Azure output blob
    :type outCourseReport: Out[bytes]
    :param outHistoricSkills: Azure output blob
    :type outHistoricSkills: Out[bytes]
    :param outLatestSkills: Azure output blob
    :type outLatestSkills: Out[bytes]
    :param outSkillsDict: Azure output blob
    :type outSkillsDict: Out[bytes]
    :raises Exception: Empty blob alert
    :raises Exception: Json empty alert
    """
    input_json = inCourseReport.read().decode('utf-8')

    if input_json == '':
        raise Exception('Blob is empty, check json output from collector')

    input_obj = json.loads(input_json)

    if len(input_obj) == 0:
        raise Exception('Unprocessed json is empty, check json output from collector')

    locations = input_obj.pop(0)

    input = json.dumps(input_obj)
    input_df = pd.read_json(input)

    bootcamps_df = process_course_data(input_df, locations["uk_locations"], inSkillsDict, outSkillsDict)
    logging.info('Successfully processed course data')
    bootcamps_csv = bootcamps_df.to_csv()
    outCourseReport.set(bootcamps_csv.encode('utf-8'))

    skills_df = process_skills_data(bootcamps_df)
    logging.info('Successfully processed skills data')
    skills_csv = skills_df.to_csv()
    outHistoricSkills.set(skills_csv.encode('utf-8'))
    outLatestSkills.set(skills_csv.encode('utf-8'))
