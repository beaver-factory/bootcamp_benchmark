from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import json
import requests
from azure.functions import InputStream
import logging


def collector_adzuna(inBlob: InputStream) -> str:
    """Makes calls to Adzuna API to find the number of jobs listed for each skill.

    :param inBlob: takes a csv file of a list of skills from the most recent Course Report scrape: latest_course_report_skills.csv
    :type inBlob: InputStream
    :raises Exception: Empty skill list alert
    :return: A json object string featuring keys of each skill and a count of the number of job ads on Adzuna featuring that skill
    :rtype: str
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
        keyword_variants = create_keyword_variants(keyword)

        keyword_query = create_keyword_query(keyword, keyword_variants)

        request_url = f"http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id_secret}&app_key={app_key_secret}&{keyword_query}&location0=UK&category=it-jobs&content-type=application/json"

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


def create_keyword_variants(keyword: str) -> str:
    """Takes a keyword and adds possible variants to include in an API search

    :param keyword: skill keyword
    :type keyword: str
    :return: skill keyword with possible variants separated by a space
    :rtype: str
    """
    processed_keywords = keyword

    # JavaScript skill processing
    if ".js" in keyword:
        processed_keywords += f" {keyword.split('.')[0]}"
    elif keyword[-2:] == "JS":
        processed_keywords += f" {keyword[:-2]}"

    return processed_keywords


def create_keyword_query(keyword: str, variant_keywords: str) -> str:
    """Takes the original keyword and the keyword with variants and returns the correct query for an API call

    :param keyword: original keyword
    :type keyword: str
    :param variant_keywords: keywords with variants
    :type variant_keywords: str
    :return: correct search query for the type of keyword given
    :rtype: str
    """
    search_param = "what="

    if keyword != variant_keywords:
        # If multiple variants have been added to the search, results should check for each version independently
        search_param = "what_or="
    elif len(keyword.split(" ")) > 1:
        # If skill has multiple words, results must include all words
        search_param = "what_phrase="

    keyword_query = search_param + variant_keywords

    return keyword_query
