import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    try:
        post = json.loads(event['body'])
        action = post['action']
        url = post['url']
    except:
        return {'statusCode': 401,
        'body': json.dumps("data missing")}
    
    if action == "resize":
        sqs = boto3.client('sqs')
        link = sqs.get_queue_url(QueueName="resize.fifo")['QueueUrl']
        sqs.send_message(QueueUrl=link , MessageBody=url , MessageGroupId="1" , MessageDeduplicationId=url)
        return {
        'statusCode': 200,
        'body': json.dumps("message sent to resize.fifo SQS")
    }

    if action == "download":
        sqs = boto3.client('sqs')
        link = sqs.get_queue_url(QueueName="download.fifo")['QueueUrl']
        sqs.send_message(QueueUrl=link , MessageBody=url , MessageGroupId="1" , MessageDeduplicationId=url)
        return {
        'statusCode': 200,
        'body': json.dumps("message sent to download.fifo SQS")
    }

    return {
        'statusCode': 401,
        'body': json.dumps("Bad REQUEST")
    }