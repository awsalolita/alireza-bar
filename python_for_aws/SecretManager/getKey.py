import boto3
import json

secrets_manager_client = boto3.client('secretsmanager')
def get_secret(secret_name):
    response = secrets_manager_client.get_secret_value(SecretId=secret_name)
    secret = response['SecretString']
    return json.loads(secret)

secret_name = 'your_secret_name_here'
db_credentials = get_secret(secret_name)