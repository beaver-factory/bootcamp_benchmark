from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os

load_dotenv()

vault_URI = os.environ["VAULT_URI"]

credential = DefaultAzureCredential()

secret_client = SecretClient(vault_url=vault_URI, credential=credential)

secret = secret_client.get_secret("adzunaAppId")

print(secret.name)
