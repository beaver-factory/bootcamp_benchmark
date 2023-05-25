import pandas as pd


def app():
    course_dataframe = pd.read_json("raw_course_data.json")

    exploded_dataframe = course_dataframe.explode('courses')

    exploded_dataframe["courseName"] = exploded_dataframe.courses.apply(
        lambda x: x["name"])

    exploded_dataframe = exploded_dataframe.drop("courses", axis=1)

    print(exploded_dataframe.head())


app()
