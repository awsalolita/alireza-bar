
import boto3
import time
import math
import boto3
from boto3.dynamodb.conditions import Key, Attr
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from decimal import *
# create table
# hash pk , RANGE sort key

t = math.ceil(time.time())
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
dynamodb.create_table(TableName='mytable', KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}, {'AttributeName': 'sentiment', 'KeyType': 'RANGE'}], AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'N'}, {'AttributeName': 'sentiment', 'AttributeType': 'S'}], ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5})
table = dynamodb.Table(name='mytable')

item = {'id': Decimal(f'{t}'), 'sentiment': 'positive'}
# put item
table.put_item(Item=item)

# get item (pk and sort key needed)
table.get_item(Key=item)['Item']


items = table.scan()['Items']

## REMEMBER to check
# for i in items:
#     if "x" in i:
#         print(i)


# query only based on partiion key
table.query(KeyConditionExpression=Key('id').eq(1718991391))['Items']

# query based on partition key and sort key
table.query(KeyConditionExpression='id = :val AND sentiment = :Sval' , ExpressionAttributeValues={ ':val' : 1718991391  , ':Sval' : 'positive'} )["Items"]


# scan table and filter based on sort key NOT Efficient
table.scan( FilterExpression='sentiment = :val' , ExpressionAttributeValues={ ':val' : 'positive'})['Items']


# filter a query based on an attribute , MUST have a partition key
table.query(KeyConditionExpression='id = :val' , FilterExpression='msg = :msg' , EpressionAttributeValues={ ':val' : 1718991391 , ':msg' : 'aloooooo22'} )['Items']
table.query(KeyConditionExpression='id = :val AND sentiment = :Sval ' , FilterExpression='msg = :msg' , ExpressionAttributeValues={ ':val' : 1718991391 , ':msg' : 'aloooooo22' , ':Sval' : 'positive' } )['Items']

# filter a scan based on an attribute , 
table.scan(FilterExpression='msg = :msg' , ExpressionAttributeValues={ ':msg' : 'aloooooo22' } )['Items']

# Query based on Global Secondary Index
table.query(IndexName='msg-index' ,KeyConditionExpression='msg = :msg' , ExpressionAttributeValues={ ':msg' : 'aloooooo22'} )['Items']


# update item (only attributes can be updated) , both pk and sk are immutable and needed
new_message = 'Updated message content here'

table.update_item(
    Key={
        'id': 1718991391,
        'sentiment': 'positive'
    },
    UpdateExpression='SET msg = :val1',
    ExpressionAttributeValues={
        ':val1': new_message
    }
)

table.update_item(
    Key={
        'improvement': improvement,
        'region': region
    },
    UpdateExpression="ADD total_votes :votevalue",
    ExpressionAttributeValues={
        ':votevalue': 1
    }
)