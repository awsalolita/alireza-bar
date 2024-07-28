import json
import base64
import gzip
import boto3
def lambda_handler(event, context):
    # TODO implement
    
    # print("*******", event)
    
        
    for i in event["Records"]:
        
        partitionKey = i["kinesis"]["partitionKey"]
        
        data = base64.b64decode(i["kinesis"]["data"])
        data = gzip.decompress(data)
        # print(data)
        
        client = boto3.client('kinesis')

        response = client.put_record(
            StreamName='processed_security_logs',
            Data=data,
            PartitionKey=partitionKey
        )
    
    # get the seq number of the last record
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
