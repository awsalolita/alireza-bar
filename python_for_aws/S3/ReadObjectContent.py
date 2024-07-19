import boto3
import json
import os



bucket_name = os.environ['bucketName']
filename='locationString.txt'
s3 = boto3.resource('s3')

obj = s3.Object(bucket_name , filename)
body = obj.get()['Body'].read().decode("utf-8")