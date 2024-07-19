# Identity Pool to User Pool
* create a `user pool` and a user inside it , then create `identity pool` for connecting them to iam 
* enable `AuthFlows`
* there are attributes for a user like the group that the user is in to choose iam based on them
### Admin user and creating custom principles(Claims)
* Creating Admin user 
```python
import boto3
client = boto3.client('cognito-idp') 

response = client.admin_create_user(
    UserPoolId='us-east-1_4Uq9pgWp1',
    Username='arpjoker3',
    TemporaryPassword='12345678'
)
```
* initiate auth
```python
response = client.admin_initiate_auth(UserPoolId='us-east-1_4Uq9pgWp1' ,
    ClientId='40uinkrbh1dqm7g0kqs9kgtlem' ,
    AuthFlow='ADMIN_USER_PASSWORD_AUTH',
    AuthParameters={        
       'USERNAME': 'arpjoker2',
        'PASSWORD': '12345678'
        })
id_token = response['AuthenticationResult']['IdToken']
```
* Create Custom Claims (`custom:rank` here)
```python
client.add_custom_attributes(
    UserPoolId='us-east-1_4Uq9pgWp1',
        CustomAttributes=[
        {
            'Name': 'rank',
            'AttributeDataType': 'String'}
    ])
```
* See Claims
```python
import jwt
jwt.decode(id_token, options={"verify_signature": False})
```

### Getting iam from idp
* get accesstoken and id_token from `userPool` 
```python
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
```
* (optional) Extract id_tokens from user and see the claims
```python
response = client.get_user(
    AccessToken=accesstoken
)
```
* Authenticate to `idp` to get `Identityid`
```python
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
```
* Assume Role (s3 example)
```python
access_key_id = response['Credentials']['AccessKeyId']
secret_access_key = response['Credentials']['SecretKey']
session_token = response['Credentials']['SessionToken']

s3 = boto3.client('s3', aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key,
                        aws_session_token=session_token)

# Example usage
response = s3.list_buckets()
print(response)
```



# using on alb
* with LB
```
<domain>/oauth2/idpresponse
```

* trust policy for the role
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "cognito-identity.amazonaws.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "cognito-identity.amazonaws.com:aud": "<ARN>"
                },
                "ForAnyValue:StringLike": {
                    "cognito-identity.amazonaws.com:amr": "authenticated"
                }
            }
        }
    ]
}
```