import pandas as pd


def app(course_dataframe):

    df = course_dataframe.explode('provider_courses').reset_index()

    normalised_df = pd.json_normalize(df.provider_courses)

    concat_normalised_df = pd.concat([df, normalised_df], axis=1).drop(
        ['provider_courses', 'provider_locations'], axis=1)

    exploded_locations = concat_normalised_df.explode(
        'course_skills').reset_index().drop(['index', 'level_0'], axis=1)

    normalised_meta = pd.concat([exploded_locations, pd.json_normalize(
        exploded_locations.meta)], axis=1).drop('meta', axis=1)

    exploded_tracks = normalised_meta.explode(
        'provider_tracks').reset_index().drop(['index'], axis=1)

    return exploded_tracks


app()
