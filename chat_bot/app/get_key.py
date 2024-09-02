from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
import os


def get_openai_key():

    credential = ManagedIdentityCredential(client_id="1f198008-886a-4016-8382-05e4bd8948b0")

    key_vault_name = "kv-i-xtech"
    key_vault_url = f"https://{key_vault_name}.vault.azure.net"

    client = SecretClient(vault_url=key_vault_url, credential=credential)

    os.environ['OPENAI_API_KEY'] = client.get_secret("OPENAI-API-KEY").value
