from pandas import DataFrame
from azure.functions import Out
from typing import Dict
import json


def process_skill_synonyms(df: DataFrame, skills_dict: Dict, outBlob: Out[bytes]) -> DataFrame:
    """Checks a course report dataframe with skills for synonyms and alters it according to a dictionary.

    :param df: a pandas dataframe
    :type df: DataFrame
    :param skills_dict: a skills dictionary
    :type skills_dict: InputStream
    :param outBlob: an azure output blob
    :type outBlob: Out[bytes]
    :raises Exception: empty dict blob warning (checking for existence of dictionary)
    :raises Exception: non-matching df lengths warning
    :return: a new pandas dataframe
    :rtype: DataFrame
    """

    # handle input

    new_skills_dict = skills_dict.copy()

    new_df = df.copy(deep=True)
    new_df.dropna(subset=['course_skills'], inplace=True)

    course_skills = new_df["course_skills"].tolist()

    check_skills = [str(skill).lower() for skill in course_skills]

    # dict checker
    for index in range(len(course_skills)):
        skill = handle_known_suffixes(check_skills[index])

        for key, value in skills_dict.items():
            if skill in value:
                course_skills[index] = key
                break
        else:
            actual_skill = str(course_skills[index])

            if skill == actual_skill.lower():
                new_skills_dict[actual_skill] = [skill]
            else:
                new_skills_dict[skill] = [skill]

    # handle output
    if set(new_skills_dict.keys()) - set(skills_dict.keys()):
        output = json.dumps(new_skills_dict)
        outBlob.set(output.encode('utf-8'))

    if len(course_skills) == len(new_df):
        new_df["course_skills"] = course_skills
        return new_df
    else:
        raise Exception('Row count of new dataframe does not match original dataframe')


def handle_known_suffixes(skill: str) -> str:
    """handles known problematic suffixes, removing them from a string appropriately

    :param skill: string of a tech skill
    :type skill: str
    :return: updated string
    :rtype: str
    """

    # if skill is one of these, early return
    full_skill_names = ['json', 'js', '.net']

    if skill in full_skill_names:
        return skill

    # otherwise, check the suffix blacklist
    unwanted_suffixes = ['.js', 'js', '.net']

    for substr in unwanted_suffixes:
        if substr in skill and f".{substr}" not in skill:
            return skill[:-len(substr)]

    return skill
