import pandas as pd
import logging


def process_course_data(unprocessed_dataframe, locations):
    """
    Returns a processed DataFrame.

        Argument:
        course_dataframe(DataFrame): A pandas DataFrame of data structure found in template_data_structure.json
        Return:
        processed_dataframe(DataFrame): A pandas DataFrame containing processed course data
    """

    # convert array of course objects to rows
    exploded_courses = unprocessed_dataframe.explode(
        'provider_courses').reset_index()

    normalised_courses = pd.json_normalize(exploded_courses.provider_courses)

    concat_dataframe_with_courses = pd.concat([exploded_courses, normalised_courses], axis=1).drop([
        'provider_courses', 'provider_locations', 'provider_tracks'], axis=1)

    logging.info('Successfully added each course of provider_courses into dataframe and removed the following columns: provider_courses, provider_locations, provider_tracks')

    exploded_skills = concat_dataframe_with_courses.explode(
        'course_skills').reset_index().drop(['index', 'level_0'], axis=1)

    logging.info('Successfully exploded course skills array into rows')

    # adding metadata to dataframe
    normalised_meta = pd.json_normalize(exploded_skills.meta)

    concat_dataframe_with_meta = pd.concat(
        [exploded_skills, normalised_meta], axis=1).drop('meta', axis=1)

    logging.info('Successfully added meta data to dataframe')

    # handle locations
    concat_dataframe_with_meta['course_locations'] = concat_dataframe_with_meta['course_locations'].map(lambda x: x.split(', '))

    exploded_locations = concat_dataframe_with_meta.explode('course_locations')

    locations.append('Online')

    exploded_locations_filtered = exploded_locations[exploded_locations['course_locations'].isin(locations)]

    logging.info('Successfully filtered course_locations by locations taken from spider')

    exploded_locations_filtered.loc[:, ('course_country',)] = 'UK'

    return exploded_locations_filtered


def process_skills_data(unprocessed_dataframe):
    """
    Returns a processed DataFrame.

        Argument:
        course_dataframe(DataFrame): A pandas DataFrame of data structure found in template_data_structure.json
        Return:
        processed_dataframe(DataFrame): A pandas DataFrame containing processed skills data
    """

    if unprocessed_dataframe.empty:
        raise Exception('Unprocessed dataframe is empty, check json output from collector')

    exploded_courses = unprocessed_dataframe.explode(
        'provider_courses').reset_index()

    normalised_courses = pd.json_normalize(exploded_courses.provider_courses)

    skills_df = normalised_courses['course_skills'].explode('course_skills').drop_duplicates().reset_index().drop('index', axis=1)

    return skills_df
