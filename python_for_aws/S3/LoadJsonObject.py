import boto3 
import json

s3 = boto3.client('s3')
s3_bucket = 'bucket'

key = 'this/is/a/key.json'
object = s3.get_object(
                Bucket = s3_bucket,
                Key = key
            )
object_data = json.loads(object['Body'].read())
