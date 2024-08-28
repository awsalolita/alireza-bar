# Assuming AWS CLI is installed and configured with necessary permissions
#echo 'aws sqs send-message --queue-url YOUR_SQS_QUEUE_URL --message-body "SSH login detected on `hostname`" ' >> /etc/profile

#!/bin/bash
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
INSTANCE_ID=`curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id`
aws sqs send-message --queue-url YOUR_SQS_QUEUE_URL --message-body "{\"instanceId\": \"$INSTANCE_ID\"}"


# lambda function
import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    for record in event['Records']:
        message_body = json.loads(record['body'])
        instance_id = message_body['instanceId']
        
        # To shut down the instance
        ec2.stop_instances(InstanceIds=[instance_id])
        
        # Or to apply a restrictive security group
        # ec2.modify_instance_attribute(InstanceId=instance_id, Groups=['YOUR_RESTRICTIVE_SG_ID'])

        print(f"Action taken on instance {instance_id}")
