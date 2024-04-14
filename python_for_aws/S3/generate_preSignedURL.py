import boto3

s3 = boto3.client('s3')

url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': 'cloudberry-examples',
        'Key': 'invoices/user1234/july2018.pdf'
    }
)
print(url)
