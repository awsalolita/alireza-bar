import boto3

# Initialize the CognitoIdentityProvider client
client = boto3.client('cognito-idp')

# Authenticate user and get tokens
response = client.initiate_auth(
    ClientId='your_client_id',
    AuthFlow='USER_PASSWORD_AUTH',
    AuthParameters={
        'USERNAME': 'user@example.com',
        'PASSWORD': 'password'
    }
)

# Extract tokens
id_token = response['AuthenticationResult']['IdToken']

# Get identity ID using tokens
cognito_identity = boto3.client('cognito-identity', region_name='your_cognito_region')
identity_pool_id = 'your_identity_pool_id'

# Get identity ID associated with the user from Cognito User Pool
response = cognito_identity.get_id(
    IdentityPoolId=identity_pool_id,
    Logins={
        'cognito-idp.your_cognito_region.amazonaws.com/your_user_pool_id': id_token
    }
)

identity_id = response['IdentityId']

# Get temporary credentials for the identity
response = cognito_identity.get_credentials_for_identity(
    IdentityId=identity_id,
    Logins={
        'cognito-idp.your_cognito_region.amazonaws.com/your_user_pool_id': id_token
    }
)

access_key_id = response['Credentials']['AccessKeyId']
secret_access_key = response['Credentials']['SecretKey']
session_token = response['Credentials']['SessionToken']

# Now you can use these credentials to access AWS services
s3 = boto3.client('s3', aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key,
                        aws_session_token=session_token)

# Example usage
response = s3.list_buckets()
print(response)
