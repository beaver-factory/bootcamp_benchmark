import pandas as pd
from pandas import DataFrame
from typing import List
from azure.functions import Out
import logging
from processor_course_report.extract_skills import extract_skills
from processor_course_report.skill_synonym_unifier import process_skill_synonyms
from typing import Dict


def process_course_data(unprocessed_dataframe: DataFrame, locations: List[str], skills_dict: Dict, outSkillsDict: Out[bytes]) -> DataFrame:
    """Processes a dataframe of course data, cleaning it and arranging it for db insertion.

    :param unprocessed_dataframe: A pandas DataFrame of data structure found in template_data_structure.json
    :type unprocessed_dataframe: DataFrame
    :param locations: list of GB locations
    :type locations: List[str]
    :param skills_dict: skills dictionary
    :type skills_dict: Dict
    :param outSkillsDict:  Azure output blob
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
    extracted_skills = process_course_descriptions(df_with_courses, skills_dict)

    df_with_skills = process_course_report_skills(extracted_skills)

    df_with_meta = process_course_report_metadata(df_with_skills)

    df_with_locations = process_course_report_locations(df_with_meta, locations)

    df_with_deduped_skills = process_skill_synonyms(df_with_locations, skills_dict, outSkillsDict)

    return df_with_deduped_skills.drop_duplicates()


def process_course_report_courses(exploded_df: DataFrame, normalised_df: DataFrame) -> DataFrame:
    """Combines initial dataframe with normalised dataframe and removes unwanted columns

    :param exploded_df: initial df
    :type exploded_df: DataFrame
    :param normalised_df: normalised provider_courses df
    :type normalised_df: DataFrame
    :return: concatenated dataframe
    :rtype: DataFrame
    """

    concat_dataframe_with_courses = pd.concat([exploded_df, normalised_df], axis=1).drop([
        'provider_courses', 'provider_locations', 'provider_tracks'], axis=1)

    logging.info('Successfully added each course of provider_courses into dataframe and removed the following columns: provider_courses, provider_locations, provider_tracks')

    return concat_dataframe_with_courses


def process_course_report_skills(df: DataFrame) -> DataFrame:
    """Explodes skills to be on separate rows, returning new dataframe

    :param df: pandas dataframe
    :type df: DataFrame
    :return: new dataframe with skills exploded
    :rtype: DataFrame
    """

    exploded_skills = df.explode(
        'course_skills').reset_index().drop(['index', 'level_0'], axis=1)

    logging.info('Successfully exploded course skills array into rows')

    return exploded_skills


def process_course_report_metadata(df: DataFrame) -> DataFrame:
    """Normalises and concatenates metadata to the dataframe

    :param df: pandas dataframe
    :type df: DataFrame
    :return: new dataframe with concatenated metadata
    :rtype: DataFrame
    """

    normalised_meta = pd.json_normalize(df.meta)

    concat_dataframe_with_meta = pd.concat(
        [df, normalised_meta], axis=1).drop('meta', axis=1)

    logging.info('Successfully added meta data to dataframe')

    return concat_dataframe_with_meta


def process_course_report_locations(df: DataFrame, locations: List[str]) -> DataFrame:
    """Explodes course_locations then filters for UK + online locations

    :param df: pandas dataframe
    :type df: DataFrame
    :param locations: list of valid UK locations
    :type locations: List[str]
    :return: new dataframe with exploded and filtered locations
    :rtype: DataFrame
    """
    df['course_locations'] = df['course_locations'].map(lambda x: x.split(', '))

    exploded_locations = df.explode('course_locations')

    locations.append('Online')

    exploded_locations_filtered = exploded_locations[exploded_locations['course_locations'].isin(locations)]

    logging.info('Successfully filtered course_locations by locations taken from spider')

    exploded_locations_filtered.loc[:, ('course_country',)] = 'UK'

    return exploded_locations_filtered


def process_course_descriptions(normalised_courses: DataFrame, skills_dict: Dict) -> DataFrame:
    """Extracts key skills from description and drops description

    :param normalised_courses: pandas dataframe
    :type normalised_courses: DataFrame
    :param inSkillsDict: Dictionary of skills
    :type inSkillsDict: InputStream
    :return: new dataframe with description dropped
    :rtype: DataFrame
    """

    def consolidate_desc_into_skills(row):
        extracted_skills = extract_skills(str(row['course_description']), skills_dict)

        existing_skills = row['course_skills']

        row['course_skills'] = list(set(existing_skills + extracted_skills))

        return row

    consolidated_skills = normalised_courses.apply(lambda x: consolidate_desc_into_skills(x), axis=1)

    desc_removed = consolidated_skills.drop('course_description', axis=1)

    return desc_removed
