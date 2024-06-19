import boto3

# Initialize the CognitoIdentityProvider client
client = boto3.client('cognito-idp')    

# Authenticate user and get tokens
response = client.initiate_auth(
    ClientId='40uinkrbh1dqm7g0kqs9kgtlem',
    AuthFlow='USER_PASSWORD_AUTH',
    AuthParameters={
        'USERNAME': 'arpjoker',
        'PASSWORD': '12345678'
    }
)

accesstoken = response['AuthenticationResult']['AccessToken']
id_token = response['AuthenticationResult']['IdToken']
## Admin user
# response = client.admin_create_user(
#     UserPoolId='us-east-1_4Uq9pgWp1',
#     Username='arpjoker3',
#     TemporaryPassword='12345678'
# )
## login after this
# response = client.admin_initiate_auth(UserPoolId='us-east-1_4Uq9pgWp1' ,
#     ClientId='40uinkrbh1dqm7g0kqs9kgtlem' ,
#     AuthFlow='ADMIN_USER_PASSWORD_AUTH',
#     AuthParameters={        
#        'USERNAME': 'arpjoker2',
#         'PASSWORD': '12345678'
#         })
# id_token = response['AuthenticationResult']['IdToken']
## create  attributes , MAKE sure you change application integration to read the custom:rank principle
# client.add_custom_attributes(
#     UserPoolId='us-east-1_4Uq9pgWp1',
#         CustomAttributes=[
#         {
#             'Name': 'rank',
#             'AttributeDataType': 'String'}
#     ])
# extract the claims
# import jwt
# jwt.decode(id_token, options={"verify_signature": False})
# Extract tokens
# response = client.get_user(
#     AccessToken=accesstoken
# )



# Get identity ID using tokens
cognito_identity = boto3.client('cognito-identity')
identity_pool_id = 'us-east-1:f7afcf7d-eb46-4644-b956-e0ac3f94ccc7'
user_pool_id =  'us-east-1_4Uq9pgWp1'
region = 'us-east-1'
# Get identity ID associated with the user from Cognito User Pool
response = cognito_identity.get_id(
    IdentityPoolId=identity_pool_id,
    Logins={
        f'cognito-idp.{region}.amazonaws.com/{user_pool_id}': id_token
    }
)

identity_id = response['IdentityId']

# Get temporary credentials for the identity
response = cognito_identity.get_credentials_for_identity(
    IdentityId=identity_id,
    Logins={
        f'cognito-idp.{region}.amazonaws.com/{user_pool_id}': id_token
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
