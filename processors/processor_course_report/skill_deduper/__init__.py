import pandas as pd
import os
import openai
import json


def skill_deduper(df):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    skills_list = df["skills"][0]

    # essential steps:
    # sort alphabetically
    alpha_skills = sorted(skills_list)
    # lowercase everything
    lower_skills = [x.lower() for x in alpha_skills]
    # only unique values
    prepared_skills_list = list(dict.fromkeys(lower_skills))

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

    response_string = response.choices[0].text
    actual = response_string.split(', ')

    return pd.DataFrame([{"skills": actual}])
