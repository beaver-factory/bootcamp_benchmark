from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import logging


def collect_adzuna():

    vault_URI = f'https://{os.environ["KeyVaultName"]}.vault.azure.net'

    credential = DefaultAzureCredential()

    secret_client = SecretClient(vault_url=vault_URI, credential=credential)

    secret = secret_client.get_secret("adzunaAppId")

    logging.info(secret.name)
