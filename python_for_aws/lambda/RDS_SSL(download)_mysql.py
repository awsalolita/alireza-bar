import os
import requests
import boto3
import sqlalchemy
from sqlalchemy import create_engine , text
from datetime import datetime, timedelta

os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
# Generate an authentication token
def generate_db_auth_token(region, hostname, port, username):
    rds = boto3.client('rds', region_name=region)
    return rds.generate_db_auth_token(
        DBHostname=hostname,
        Port=port,
        DBUsername=username,
        Region=region
    )

def download_certificate(url, path):
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)

def lambda_handler(event, context):
    # Settings
    region = 'us-east-1'
    hostname = 'database-1-instance-1.cjiy4mo6sjrh.us-east-1.rds.amazonaws.com'
    port = 3306
    username = 'jane_doe'
    database_name = 'mysql'
    #https://s3.amazonaws.com/rds-downloads/rds-ca-2019-root.pem
    cert_url = 'https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem'
    cert_path = '/tmp/global-bundle.pem'
    
    # Download the SSL certificate
    if not os.path.exists(cert_path):
        download_certificate(cert_url, cert_path)

    # Generate the auth token
    token = generate_db_auth_token(region, hostname, port, username)
    
    # Database URL with IAM auth token
    database_url = sqlalchemy.engine.url.URL.create(
        drivername="mysql+mysqlconnector",
        username=username,
        password=token,
        host=hostname,
        port=port,
        database=database_name,
        query={
            'ssl_ca': cert_path
        }
    )
    
    # Create engine and connect to the database
    engine = create_engine(database_url, echo=True)
    connection = engine.connect()

    try:
        # Execute a query
        result = connection.execute(text("SELECT CURRENT_USER();"))
        current_user = result.fetchone()
        print(current_user)
    finally:
        connection.close()

    return {
        'statusCode': 200,
        'body': "Database query executed successfully using IAM authentication"
    }
