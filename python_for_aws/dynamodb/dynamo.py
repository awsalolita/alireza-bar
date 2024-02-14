import boto3
import time
import math

# create table
# hash pk , RANGE sort key
import boto3
t = math.ceil(time.time())
dynamodb = boto3.client('dynamodb', region_name='us-east-1')
dynamodb.create_table(TableName='mytable', KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}, {'AttributeName': 'sentiment', 'KeyType': 'RANGE'}], AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'N'}, {'AttributeName': 'sentiment', 'AttributeType': 'S'}], ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5})

# put item
dynamodb.put_item(TableName='mytable', Item={'id': {'N': f'{t}' }, 'sentiment': {'S': 'positive'}})

# get item
dynamodb.get_item(TableName='mytable    ', Key={'id': {'N': f'{t}'}, 'sentiment': {'S': 'positive'}})['Item']

## scan all items in the table
dynamodb = boto3.resource('dynamodb' , region_name='us-east-1' )
table = dynamodb.Table('mytable')

items = table.scan()['Items']

for i in items:
    if "x" in i:
        print(i)


# import one item
# N number S string
table.put_item(Item={'id' : t , 'sentiment' : 'ljlkjljlkjl'} )

