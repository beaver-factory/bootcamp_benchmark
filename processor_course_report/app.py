import pandas as pd


def find_time_commitment(x):
    """
    Returns a string of the time commitment or None.

        Argument:
        x(Series): A pandas Series containing the course names
        Returns:
        time_commitment(str): A string of the time commitment found in the course name
        time_commitment(None): If no time commitment found in the course name
    """

    if not isinstance(x.course_name, str):
        return None
    if 'part time' in x.course_name.lower():
        return 'part_time'
    if 'full time' in x.course_name.lower():
        return 'full_time'
    else:
        return None


def process_scraped_data(unprocessed_dataframe):
    """
    Returns a processed DataFrame.

        Argument:
        course_dataframe(DataFrame): A pandas DataFrame of data structure found in template_data_structure.json
        Return:
        processed_dataframe(DataFrame): A pandas DataFrame containing processed course data
    """

    exploded_courses = unprocessed_dataframe.explode(
        'provider_courses').reset_index()

    normalised_courses = pd.json_normalize(exploded_courses.provider_courses)

    concat_dataframe_with_courses = pd.concat([exploded_courses, normalised_courses], axis=1).drop([
        'provider_courses', 'provider_locations'], axis=1)

    concat_dataframe_with_courses['time'] = concat_dataframe_with_courses.apply(
        lambda x: find_time_commitment(x), axis=1)

    exploded_skills = concat_dataframe_with_courses.explode(
        'course_skills').reset_index().drop(['index', 'level_0'], axis=1)

    normalised_meta = pd.json_normalize(exploded_skills.meta)

    concat_dataframe_with_meta = pd.concat(
        [exploded_skills, normalised_meta], axis=1).drop('meta', axis=1)

    exploded_tracks = concat_dataframe_with_meta.explode(
        'provider_tracks').reset_index().drop(['index'], axis=1)

    exploded_tracks['course_locations'] = exploded_tracks['course_locations'].map(
        lambda x: x.split(', '))

    processed_dataframe = exploded_tracks.explode('course_locations')

    return processed_dataframe
