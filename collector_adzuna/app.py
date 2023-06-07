from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import json
import requests
import azure.functions as func


def collector_adzuna(inBlob: func.InputStream):

    skills_csv_string = inBlob.read()

    unformatted_skills_list = "".join(skills_csv_string).split("\n")

    list_of_keywords = []

    for skill in unformatted_skills_list:
        if skill != "" and skill != ",course_skills":
            formatted_skill = skill.split(",")[1]
            list_of_keywords.append(formatted_skill)

    vault_URI = f'https://{os.environ["KeyVaultName"]}.vault.azure.net'

    credential = DefaultAzureCredential()

    secret_client = SecretClient(vault_url=vault_URI, credential=credential)

    app_id_secret = secret_client.get_secret("adzunaAppId")

    app_key_secret = secret_client.get_secret("adzunaAppKey")

    # Get request to adzuna for each keyword

    skill_count = {}

    for keyword in list_of_keywords:
        request_url = f"http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id_secret.value}&app_key={app_key_secret.value}&what={keyword}&location0=UK&content-type=application/json"

        request = requests.get(request_url)

        request_json = request.json()

        job_count = request_json['count']

        skill_count[keyword] = job_count

    return json.dumps(skill_count)
