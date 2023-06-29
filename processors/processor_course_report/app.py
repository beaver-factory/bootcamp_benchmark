import pandas as pd
import logging
from processor_course_report.extract_skills import extract_skills
from processor_course_report.skill_deduper import check_edge_case_dict
import json


def process_course_data(unprocessed_dataframe, locations, inSkillsDict, outSkillsDict):
    """Processes a dataframe of course data, cleaning it and arranging it for db insertion.

    :param unprocessed_dataframe: A pandas DataFrame of data structure found in template_data_structure.json
    :type unprocessed_dataframe: DataFrame
    :param locations: list of GB locations
    :type locations: list
    :param inSkillsDict: Azure input blob
    :type inSkillsDict: InputStream
    :param outSkillsDict: Azure output blob
    :type outSkillsDict: Out[bytes]
    :return: a pandas DataFrame containing processed course data
    :rtype: DataFrame
    """

    # convert array of course objects to rows
    exploded_courses = unprocessed_dataframe.explode(
        'provider_courses').reset_index()

    normalised_courses = pd.json_normalize(exploded_courses.provider_courses)

    # combine different aspects of the data into the dataframe
    df_with_courses = process_course_report_courses(exploded_courses, normalised_courses)

    # extract skills from description
    extracted_skills = process_course_descriptions(df_with_courses, inSkillsDict)

    df_with_skills = process_course_report_skills(extracted_skills)

    df_with_meta = process_course_report_metadata(df_with_skills)

    df_with_locations = process_course_report_locations(df_with_meta, locations)

    df_with_deduped_skills = check_edge_case_dict(df_with_locations, inSkillsDict, outSkillsDict)

    return df_with_deduped_skills


def process_course_report_skills(df):
    exploded_skills = df.explode(
        'course_skills').reset_index().drop(['index', 'level_0'], axis=1)

    logging.info('Successfully exploded course skills array into rows')

    return exploded_skills


def process_course_report_courses(exploded_df, normalised_df):
    concat_dataframe_with_courses = pd.concat([exploded_df, normalised_df], axis=1).drop([
        'provider_courses', 'provider_locations', 'provider_tracks'], axis=1)

    logging.info('Successfully added each course of provider_courses into dataframe and removed the following columns: provider_courses, provider_locations, provider_tracks')

    return concat_dataframe_with_courses


def process_course_report_metadata(df):
    normalised_meta = pd.json_normalize(df.meta)

    concat_dataframe_with_meta = pd.concat(
        [df, normalised_meta], axis=1).drop('meta', axis=1)

    logging.info('Successfully added meta data to dataframe')

    return concat_dataframe_with_meta


def process_course_report_locations(df, locations):
    df['course_locations'] = df['course_locations'].map(lambda x: x.split(', '))

    exploded_locations = df.explode('course_locations')

    locations.append('Online')

    exploded_locations_filtered = exploded_locations[exploded_locations['course_locations'].isin(locations)]

    logging.info('Successfully filtered course_locations by locations taken from spider')

    exploded_locations_filtered.loc[:, ('course_country',)] = 'UK'

    return exploded_locations_filtered


def process_course_descriptions(normalised_courses, inSkillsDict):
    skills_dict = json.loads(inSkillsDict.read().decode('utf-8'))

    def consolidate_desc_into_skills(row):
        extracted_skills = extract_skills(str(row['course_description']), skills_dict)

        existing_skills = row['course_skills']

        row['course_skills'] = list(set(existing_skills + extracted_skills))

        return row

    normalised_courses.apply(lambda x: consolidate_desc_into_skills(x), axis=1)

    desc_removed = normalised_courses.drop('course_description', axis=1)

    return desc_removed
