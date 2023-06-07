from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
# remove below on deployment
from dotenv import load_dotenv
import requests

# remove on deployment
load_dotenv()


def collector_adzuna(list_of_keywords):

    # Get Adzuna app id/key secrets from key vault

    vault_URI = f'https://{os.environ["KeyVaultName"]}.vault.azure.net'

    credential = DefaultAzureCredential()

    secret_client = SecretClient(vault_url=vault_URI, credential=credential)

    app_id_secret = secret_client.get_secret("adzunaAppId")

    app_key_secret = secret_client.get_secret("adzunaAppKey")

    skill_count = {}

    # Get request to adzuna for each keyword

    for keyword in list_of_keywords:
        request_url = f"http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id_secret.value}&app_key={app_key_secret.value}&what={keyword}&location0=UK&content-type=application/json"

        request = requests.get(request_url)

        request_json = request.json()

        job_count = request_json['count']

        skill_count[keyword] = job_count

    return skill_count


#  remove on deployment
print(collector_adzuna(['python', 'JavaScript']))
