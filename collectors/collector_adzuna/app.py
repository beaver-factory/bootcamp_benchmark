from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import json
import requests
from azure.functions import InputStream
import logging
import urllib.parse


def collector_adzuna(inSkillsDict: InputStream) -> str:
    """Makes calls to Adzuna API to find the number of jobs listed for each skill.

    :param inSkillsDict: takes a json file of the skills_dict
    :type inSkillsDict: InputStream
    :raises Exception: Empty skill list alert
    :return: A json object string featuring keys of each skill and a count of the number of job ads on Adzuna featuring that skill
    :rtype: str
    """

    # check input
    input_json = inSkillsDict.read().decode('utf-8')

    if input_json == "" or input_json == "{}":
        raise Exception('inSkillsDict is empty, check skills_dict.json exists')

    skills_dict = json.loads(input_json)

    app_id_secret = get_secret_value("adzunaAppId")

    app_key_secret = get_secret_value("adzunaAppKey")

    skill_count = {}

    for keyword in skills_dict:

        keyword_query = create_keyword_query(skills_dict[keyword])

        request_url = f"http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id_secret}&app_key={app_key_secret}&{keyword_query}&location0=UK&category=it-jobs&content-type=application/json&title_only=junior"

        logging.info(f'keyword = {keyword}')
        logging.info(f'keyword_query = {keyword_query}')
        logging.info(f'request_url = {request_url}')

        response = requests.get(request_url)

        if response.status_code >= 400:
            logging.warning(
                f'Adzuna API GET request failed for keyword={keyword}')
        else:
            response_json = response.json()

            job_count = response_json['count']

            skill_count[keyword] = job_count

    return json.dumps(skill_count)


def get_secret_value(secret_name: str):
    """Takes the name of a secret stored in the Azure Key Vault and returns its value

    :param secret_name: name of a secret
    :type secret_name: str
    :return: value of the given secret name
    :rtype: str
    """
    vault_URI = f'https://{os.environ["KeyVaultName"]}.vault.azure.net'

    credential = DefaultAzureCredential()

    secret_client = SecretClient(vault_url=vault_URI, credential=credential)

    secret_value = secret_client.get_secret(secret_name).value

    logging.info(f'Succesfully retrieved {secret_name} secret from vault')

    return secret_value


def create_keyword_query(synonyms: list) -> str:
    """Takes a keyword and returns synonyms if applicable with the relevant query string for the adzuna API

    :param synonyms: list of synyoms taken from skills_dict
    :type synonyms: list
    :return: query value featuring skill and synonyms
    :rtype: str
    """

    if len(synonyms) == 1:
        if ' ' not in synonyms[0]:
            # where key == value (no synonyms) and single word skill
            return 'what=' + urllib.parse.quote(synonyms[0])
        else:
            # where key == value (no synonyms) but multi-word skill
            return 'what_phrase=' + urllib.parse.quote(synonyms[0])
    elif len(synonyms) > 1:
        chars = []
        for synonym in synonyms:
            for char in synonym:
                chars.append(char)
        if ' ' in chars:
            # where multiple synyonyms and one contains a space, default to just searching using key
            return 'what=' + urllib.parse.quote(synonyms[0])
        else:
            # where multiple synonyms and no spaces, include all synonyms in query
            return 'what_or=' + urllib.parse.quote((" ").join(synonyms))
