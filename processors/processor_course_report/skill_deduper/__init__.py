import pandas as pd
import os
import openai
import json


def skill_deduper(df):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    prepared_skills_list = prep_prompt_input(df)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""Here is a list of software development technologies with lots of similar values:{prepared_skills_list}.
        Please perform the following steps in this order:
        1. Remove any values that are the same as other values but that also include an additional suffix.
        2. Remove any values that are abbreviations of other values.
        3. Remove any values that are acronyms of other values.
        4. Return the list as a series of comma separated values.
        Please return only the list and no other words or phrases.\n \n""",
        temperature=1,
        max_tokens=100,
        top_p=0.1,
        frequency_penalty=0.8,
        presence_penalty=0.0
    )

    response_string = response["choices"][0]["text"]
    actual = response_string.split(', ')

    edgy_skills = check_edge_case_dict(actual)

    return pd.DataFrame([{"skills": edgy_skills}])


def prep_prompt_input(df):

    skills_list = df["skills"][0]

    if len(skills_list) == 0:
        raise Exception("Cannot prep prompt, list of skills is empty")

    # essential steps:
    # sort alphabetically
    alpha_skills = sorted(skills_list)
    # lowercase everything
    lower_skills = [x.lower() for x in alpha_skills]
    # only unique values
    prepared_skills_list = list(dict.fromkeys(lower_skills))

    return prepared_skills_list


def check_edge_case_dict(skills_list):

    skills_to_dedupe = {
        "html5": "html",
    }

    for skill in skills_list:
        if skill in skills_to_dedupe and skills_to_dedupe[skill] in skills_list:
            skills_list.remove(skill)
        elif skill in skills_to_dedupe:
            skills_list[skills_list.index(skill)] = skills_to_dedupe[skill]

    return skills_list
