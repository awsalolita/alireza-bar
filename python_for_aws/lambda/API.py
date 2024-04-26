import boto3
import decimal
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(name='mytable')

def lambda_handler(event, context):

    
    
    # POST request    
    # event['body']
    
    path = event['rawPath']
    
    arg = path.split('/')
    
    if arg[1] == 'sentiment':
        id = arg[2]
        item = table.query(KeyConditionExpression='id = :val' , ExpressionAttributeValues={ ':val' : int(id) } )['Items']
        
    elif arg[1] == 'sentiments':
        item = table.scan()
        item = item['Items']
    
    return {
        'statusCode': 200,
        'body': item
    }
