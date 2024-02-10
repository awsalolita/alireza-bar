import boto3
import wget 
import uuid
import time

MId = "1"
QName = "download.fifo"
sqs = boto3.client('sqs')
url = sqs.get_queue_url(QueueName=QName)['QueueUrl']

while True:
    response = sqs.receive_message(QueueUrl=url,MaxNumberOfMessages=1,MessageAttributeNames=[f'MessageGroupId={MId}'],VisibilityTimeout=0,WaitTimeSeconds=20)
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    print(f"Message {message['Body']} Received , Trying to download")
    try:
        name = uuid.uuid4()
        wget.download(message['Body'] ,  out=f"/tmp/{name}")
        print(f"Downloaded {message['Body']} to /tmp/{name}")
        sqs.delete_message(QueueUrl=url,ReceiptHandle=receipt_handle)
        print(f"Deleted message {message['Body']}")

    except:
        print(f"Failed to download {message['Body']} , sleeping foir 5 seconds and retrying")
        time.sleep(5)
