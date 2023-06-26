from pandas import DataFrame
from dotenv import load_dotenv
from azure.functions import InputStream, Out
import json

load_dotenv()


def check_edge_case_dict(df: DataFrame, inBlob: InputStream, outBlob: Out[bytes]) -> DataFrame:
    # handle input
    input_json = inBlob.read().decode('utf-8')

    if input_json == "" or input_json == {}:
        raise Exception('inBlob is empty, check skills_dict.json exists')

    skills_dict = json.loads(input_json)
    new_skills_dict = skills_dict.copy()

    new_df = df.copy(deep=True)
    course_skills = new_df["course_skills"][0]

    # dict checker
    for i in range(len(course_skills)):
        skill = handle_known_suffixes(course_skills[i])
        new_df["course_skills"][0][i] = new_df["course_skills"][0][i].lower()

        try:
            key = next(key for key, value in skills_dict.items() if skill in value)
            new_df["course_skills"][0][i] = key
        except StopIteration:
            new_skills_dict[skill] = [skill]

    # handle output
    if set(new_skills_dict.keys()) - set(skills_dict.keys()):
        output = json.dumps(new_skills_dict)
        outBlob.set(output.encode('utf-8'))

    return new_df


def handle_known_suffixes(skill):
    if '.js' in skill:
        skill = skill[:-3]

    if skill != 'js' and 'js' in skill:
        skill = skill[:-2]

    if skill != '.net' and '.net' in skill:
        skill = skill[:-4]

    return skill
