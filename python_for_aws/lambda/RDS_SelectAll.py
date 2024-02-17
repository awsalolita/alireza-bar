import json
import boto3
from sqlalchemy import create_engine , text


def get_secret(secret_name):
    secrets_manager_client = boto3.client('secretsmanager')
    response = secrets_manager_client.get_secret_value(SecretId=secret_name)
    secret = response['SecretString']
    return json.loads(secret)

def lambda_handler(event, context):
    # TODO implement
    secret_name = 'rds!db-cd703933-6a03-47d6-ad30-a79a4ef175c2'
    db_credentials = get_secret(secret_name)
    write_engine = create_engine(f"mysql+mysqlconnector://{db_credentials['username']}:{db_credentials['password']}@database-1.cowxjj5b6nhn.us-east-1.rds.amazonaws.com:3306")
    con = write_engine.connect()
    try:
        con.execute(text('create database ali'))
    except:
        print('exists')
        
    con.execute(text('use ali'))
    res = con.execute(text('show databases')).fetchall()
    print("aloooooooo#######3")
    return {
        'statusCode': 200,
    }
