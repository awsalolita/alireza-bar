import boto3
import json




lambda_client = boto3.client('lambda')
# invokation type can be RequestResponse (sync) or Event (async)
invoke_response = lambda_client.invoke(FunctionName="another_lambda_", InvocationType='Event', Payload=json.dumps({'ali' : 'mmd'}))

invoke_response['Payload'].read().decode()