import pandas as pd
from pandas import DataFrame
import os
import openai
from typing import List
from dotenv import load_dotenv
import json

load_dotenv()


# def skill_deduper() -> DataFrame:
#     """Removes duplicates of skills e.g. ["React", "react.js"] becomes ["react"]

#     :param df: DataFrame containing skills
#     :type df: DataFrame
#     :return: DataFrame containing skill
#     :rtype: DataFrame
#     """
#     openai.api_key = os.environ["OPENAI_API_KEY"]

#     # skills_list = df["course_skills"][0]
#     # prepared_skills_list = prep_prompt_input(skills_list)

#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=f"""We are using python to create a list of software development technologies and programming skills, which currently includes lots of similar values:['agile', 'angular', 'angularjs', 'data engineering', 'devops', 'express', 'express.js', 'javascript', 'js', 'mysql', 'networking', 'node', 'node.js', 'nodejs', 'nodered', 'postgresql', 'postgresql', 'problem solving', 'psql', 'react', 'react.js', 'reactjs', 'sql', 'ts', 'typescript'].
#         Please perform the following steps in this order:
#         1. Remove any values from the list that are the same as other values in the list, but that also include an additional suffix.
#         2. Remove any values that are abbreviations of other values.
#         3. Remove any values that are acronyms of other values.
#         4. Return one list of unique values, and one list of the extracted related values.
#         Please return only the lists and no other words or phrases.\n \n""",
#         temperature=1,
#         max_tokens=1000,
#         top_p=0.1,
#         frequency_penalty=0.8,
#         presence_penalty=0.0
#     )

#     print('response 1:', response["choices"][0]['text'])

#     # response_string = response["choices"][0]["text"]
#     # actual = response_string[8:]
#     # print(actual)
#     # edgy_skills = check_edge_case_dict(actual)

#     # return pd.DataFrame([{"skills": edgy_skills}])


def prep_prompt_input(skills_list: List[str]) -> List[str]:
    """Performs essential preprocessing of skills list before handing to OpenAI

    :param skills_list: List of skills
    :type df: List[str]
    :raises Exception: skill list error
    :return: list of skill strings
    :rtype: List[str]
    """

    if len(skills_list) == 0:
        raise Exception("Cannot prep prompt, list of skills is empty")

    lower_skills = [x.lower() for x in skills_list]

    prepared_skills_list = list(dict.fromkeys(lower_skills))

    sorted_list = sorted(prepared_skills_list)
    print(sorted_list)


def check_edge_case_dict(skills_list: List[str]) -> List[str]:
    # INPUT course_report df and output course_report df

    skills_to_dedupe = {
        "html5": "html",
    }

    for skill in skills_list:
        if skill in skills_to_dedupe and skills_to_dedupe[skill] in skills_list:
            skills_list.remove(skill)
        elif skill in skills_to_dedupe:
            skills_list[skills_list.index(skill)] = skills_to_dedupe[skill]

    return skills_list


# prep_prompt_input(["react", "react.JS", "react.js", "React", "React.JS", "ReactJS", "posgresql", "SQL", "postgreSQL", "PSQL", "psql", "angular", "angularJS", "angularjs", "Express", "express.js", "Agile", "problem solving", "data engineering", "mysql", "devops", "Networking", "Node", "node.js", "nodeRED", "NodeJS", "js", "JavaScript", "ts", "TypeScript"])
skill_deduper()
