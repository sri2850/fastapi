from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/app/.env")
class ConfigManager:
    def __init__(self, key_vault_url):
        # print(url)
        self.client = SecretClient(vault_url=key_vault_url, credential=DefaultAzureCredential())
        self.secrets = {}
    def get_secrets(self, secret_name):
        if secret_name not in self.secrets:
            secret = self.client.get_secret(secret_name)
            self.secrets[secret_name] = secret.value
        return self.secrets[secret_name]
    def get(self, key):
        return self.get_secrets(key)


key_vault_url = os.getenv("KEY_VAULT_URL")
config_manager = ConfigManager("https://azkvfastapi.vault.azure.net/")