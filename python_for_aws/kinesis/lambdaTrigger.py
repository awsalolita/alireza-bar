import json
import boto3
import base64
def lambda_handler(event, context):
    comprehend = boto3.client('comprehend')
    
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record["kinesis"]["data"])
        post_text = payload.decode('utf-8')
        
        print(f"Processing post: {post_text}")
        print("payloooooad" , payload)
        # payload = json.loads(payload)

        # a = {"message": "Hello, Kinesis!","timestamp": "2023-04-01T12:00:00Z"}
        # payload = json.loads(a)['message']

    return {
        'statusCode': 200,
        'body': json.dumps('Sentiment analysis completed')
    }
