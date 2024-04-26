
### 8883 port for iot

import json
import time
import boto3
import math

def lambda_handler(event, context):
    message = event['msg']
    client = boto3.client('comprehend' , region_name="us-east-1")
    sen = client.detect_sentiment(Text=message , LanguageCode='en')['Sentiment']
    
    dynamodb = boto3.client('dynamodb' , region_name='us-east-1')
    t = math.ceil(time.time())
    table='mytable'
        
    dynamodb.put_item(TableName=table , Item={'id': {'N': f'{t}'}, 'sentiment': {'S': f'{sen}'}  , 'message' :  {'S' : f"{message}" } })
    
    
    
    return 200