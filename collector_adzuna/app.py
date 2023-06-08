from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import json
import requests
import azure.functions as func
import logging


def collector_adzuna(inBlob: func.InputStream):

    skills_csv_string = inBlob.read().decode('utf-8')

    logging.info(skills_csv_string)

    if len(skills_csv_string) == 0:
        raise Exception('List of skills is empty, CSV may be empty')

    unformatted_skills_list = skills_csv_string.split("\r\n")

    logging.info(unformatted_skills_list)

    list_of_keywords = []

    for skill in unformatted_skills_list:
        if skill != "" and skill != ",course_skills":
            formatted_skill = skill.split(",")[1]
            list_of_keywords.append(formatted_skill)

    app_id_secret = get_secret_value("adzunaAppId")

    app_key_secret = get_secret_value("adzunaAppKey")

    skill_count = {}

    for keyword in list_of_keywords:
        request_url = f"http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id_secret}&app_key={app_key_secret}&what={keyword}&location0=UK&content-type=application/json"

        response = requests.get(request_url)

        if response.status_code >= 400:
            logging.warning(f'Adzuna API GET request failed for keyword={keyword}')
        else:
            response_json = response.json()

            job_count = response_json['count']

            skill_count[keyword] = job_count

    return json.dumps(skill_count)


def get_secret_value(secret_name):
    vault_URI = f'https://{os.environ["KeyVaultName"]}.vault.azure.net'

    credential = DefaultAzureCredential()

    secret_client = SecretClient(vault_url=vault_URI, credential=credential)

    return secret_client.get_secret(secret_name).value
