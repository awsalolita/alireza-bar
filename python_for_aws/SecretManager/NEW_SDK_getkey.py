# pip install aws-secretsmanager-caching

import boto3
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 
import json

client = boto3.client('secretsmanager' , region_name = 'us-east-1')
cache_config = SecretCacheConfig()
cache = SecretCache( config = cache_config, client = client)
secret = cache.get_secret_string('mysecret')
a = json.loads(secret)

