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

items = dynamodb.scan(TableName='mytable')['Items']

## REMEMBER to check
# for i in items:
#     if "x" in i:
#         print(i)


# query only based on partiion key
dynamodb.query(TableName='mytable' ,KeyConditionExpression='id = :val' , ExpressionAttributeValues={ ':val' : {'S' : '1'}} )

# query based on partition key and sort key
dynamodb.query(TableName='mytable' ,KeyConditionExpression='id = :val AND sentiment = :Sval' , ExpressionAttributeValues={ ':val' : {'S' : '1'} , ':Sval' : {'S' : 'hello'}} )


# scan table and filter based on sort key NOT Efficient
dynamodb.scan(TableName='mytable' , FilterExpression='sentiment = :val' , ExpressionAttributeValues={ ':val' : {'S' : 'positive'}} )['Items']


# filter a query based on an attribute , MUST have a partition key
dynamodb.query(TableName='mytable' ,KeyConditionExpression='id = :val' , FilterExpression='message = :msg' , ExpressionAttributeValues={ ':val' : {'S' : '1'} , ':msg' : {'S' : 'aloo'}} )
dynamodb.query(TableName='mytable' ,KeyConditionExpression='id = :val AND sentiment = :Sval ' , FilterExpression='message = :msg' , ExpressionAttributeValues={ ':val' : {'S' : '1'} , ':msg' : {'S' : 'aloo'} , ':Sval' : {'S' : 'hello'} } )['Items']

# filter a scan based on an attribute , 
dynamodb.scan(TableName='mytable' , FilterExpression='message = :msg' , ExpressionAttributeValues={ ':msg' : {'S' : 'aloo'}} )['Items']

# Query based on Global Secondary Index
dynamodb.query(TableName='mytable', IndexName='message-index' ,KeyConditionExpression='message = :msg' , ExpressionAttributeValues={ ':msg' : {'S' : 'aloo'}} )['Items']


# update item (only attributes can be updated) , both pk and sk are immutable and needed
new_message = 'Updated message content here'

dynamodb.update_item(TableName='mytable' , Key={'id' : {'S' : '1'} , 'sentiment' : {'S' : 'hello'}} , UpdateExpression='SET message = :new_message' , ExpressionAttributeValues={':new_message': {'S': new_message}} , ReturnValues='UPDATED_NEW')



### STRUCTURED RESPONSE

def json_response(respDB):
  response = []
  for item in respDB['Items']:
    ## MODIFY
    # a = dec.as_integer_ratio()[0]
    response.append( { 'id': item['id'], 'message': item['message'], 'sentiment': item['sentiment']})
            
  return response