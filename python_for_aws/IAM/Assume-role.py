import boto3

# only on host with full permissions
# Create an STS client
sts_client = boto3.client('sts')

# Assume the role
assumed_role = sts_client.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/YourRoleName",
    RoleSessionName="SessionName"
)

# Extract the temporary credentials
credentials = assumed_role['Credentials']

# Use the temporary credentials to create an S3 resource
s3 = boto3.resource(
    's3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken'],
)

# Now you can use the S3 resource to interact with S3
for bucket in s3.buckets.all():
    print(bucket.name)
