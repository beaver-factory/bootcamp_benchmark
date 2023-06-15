from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import json
import requests
import azure.functions as func
import logging


def collector_adzuna(inBlob: func.InputStream):
    """
    Makes calls to Adzuna API to find the number of jobs listed for each skill.

        Argument: takes a csv file of a list of skills from the most recent Course Report scrape: latest_course_report_skills.csv
        Returns: a json object featuring keys of each skill and a count of the number of job ads on Adzuna featuring that skill
    """

    skills_csv_string = inBlob.read().decode('utf-8')

    if len(skills_csv_string) == 0:
        raise Exception('List of skills is empty, CSV may be empty')

    unformatted_skills_list = skills_csv_string.split("\n")

    list_of_keywords = []

    for skill in unformatted_skills_list:
        if skill != "" and skill != ",course_skills":
            formatted_skill = skill.split(",")[1]
            if formatted_skill != "":
                list_of_keywords.append(formatted_skill)

    logging.info(
        'Successfully read latest_course_report_skills.csv and formatted skills into list')

    app_id_secret = get_secret_value("adzunaAppId")

    app_key_secret = get_secret_value("adzunaAppKey")

    skill_count = {}

    for keyword in list_of_keywords:
        request_url = f"http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id_secret}&app_key={app_key_secret}&what={keyword}&location0=UK&category=it-jobs&content-type=application/json"

        response = requests.get(request_url)

        if response.status_code >= 400:
            logging.warning(
                f'Adzuna API GET request failed for keyword={keyword}')
        else:
            response_json = response.json()

            job_count = response_json['count']

            skill_count[keyword] = job_count

    return json.dumps(skill_count)


def get_secret_value(secret_name):
    """
    Takes the name of a secret stored in the Azure Key Vault and returns its value

        Argument: name of a secret
        Returns: value of the given secret name
    """
    vault_URI = f'https://{os.environ["KeyVaultName"]}.vault.azure.net'

    credential = DefaultAzureCredential()

    secret_client = SecretClient(vault_url=vault_URI, credential=credential)

    secret_value = secret_client.get_secret(secret_name).value

    logging.info(f'Succesfully retrieved {secret_name} secret from vault')

    return secret_value
