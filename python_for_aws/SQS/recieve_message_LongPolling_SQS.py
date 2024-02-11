import boto3
import wget 
import uuid
import time
import os

MId = "1"
QName = "download.fifo"
sqs = boto3.client('sqs' , region_name="us-east-1")
url = sqs.get_queue_url(QueueName=QName)['QueueUrl']

while True:
    response = sqs.receive_message(QueueUrl=url,MaxNumberOfMessages=1,MessageAttributeNames=[f'MessageGroupId={MId}'],VisibilityTimeout=60,WaitTimeSeconds=20)
    if 'Messages' in response and response['Messages']:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        print(f"Message {message['Body']} Received , Trying to download")
        try:
            name = uuid.uuid4()
            
            wget.download(message['Body'] ,  out=f"/tmp/{name}")
            print(f"Downloaded {message['Body']} to /tmp/{name}")

            boto3.client('s3').upload_file(f"/tmp/{name}" , "arpjoker" , f"download/{name}")
            print(f"Uploaded /tmp/{name} to S3")

            os.remove(f"/tmp/{name}")    
            
            sqs.delete_message(QueueUrl=url,ReceiptHandle=receipt_handle)
            print(f"Deleted message {message['Body']}")

        except Exception as e:
            print(e , "sleeping for 5 seconds and retrying")
            time.sleep(5)
    else:
        print("No messages in the queue")
        time.sleep(5)
