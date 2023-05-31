import pandas as pd
import json


def find_time_commitment(x):
    if 'part time' in x.course_name.lower():
        return 'part_time'
    if 'full time' in x.course_name.lower():
        return 'full_time'
    else:
        return None


def process_scraped_data(course_dataframe):
    """
    Returns a processed DataFrame.
        Argument:
        course_dataframe(DataFrame): A pandas DataFrame of data structure found in template_data_structure.json
        Return:
        processed_dataframe(DataFrame): A pandas DataFrame containing processed course data
    """
    required_fields = [
        'provider_courses',
        'provider_tracks',
    ]

    required_nested_fields = [
        "course_skills",
        "course_locations"
    ]

    for field in required_fields:
        if field not in course_dataframe:
            print(field)
            print(course_dataframe)
            raise Exception('Missing required field')


    # if type(course_dataframe.provider_courses) != 'list':
    #     raise Exception('Field is wrong datatype')

    df = course_dataframe.explode('provider_courses').reset_index()

    normalised_df = pd.json_normalize(df.provider_courses)

    concat_normalised_df = pd.concat([df, normalised_df], axis=1).drop(
        ['provider_courses', 'provider_locations'], axis=1)

    concat_normalised_df['time'] = concat_normalised_df.apply(
        lambda x: find_time_commitment(x), axis=1)

    exploded_locations = concat_normalised_df.explode(
        'course_skills').reset_index().drop(['index', 'level_0'], axis=1)

    normalised_meta = pd.concat([exploded_locations, pd.json_normalize(
        exploded_locations.meta)], axis=1).drop('meta', axis=1)

    exploded_tracks = normalised_meta.explode(
        'provider_tracks').reset_index().drop(['index'], axis=1)

    return exploded_tracks


course_dict = [{
    "provider_name": "",
    "provider_locations": [""],
    "provider_tracks": [""],
    "provider_courses": [
        {
            "course_name": "",
            "course_skills": [""],
            "course_locations": "",
            "course_desc": ""
        }
    ],
    "meta": {
        "target_url": "",
        "timestamp": ""
    }
},
    {
    "provider_name": "",
        "provider_locations": [""],
        "provider_tracks": [""],
        "provider_courses": [
            {
                "course_name": "",
                "course_skills": [""],
                "course_locations": "",
                "course_desc": ""
            }
        ],
    "meta": {
            "target_url": "",
            "timestamp": ""
            }
}
]

parsed_data = json.dumps(course_dict)

df = pd.read_json(parsed_data)

process_scraped_data(df)
