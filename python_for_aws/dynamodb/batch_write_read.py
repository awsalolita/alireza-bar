import boto3

# Initialize a Boto3 DynamoDB client
dynamodb_client = boto3.client('dynamodb')

response = dynamodb_client.batch_write_item(
    RequestItems={
        'mytable': [
            {
                'PutRequest': {
                    'Item': {
                        'id': {'S': 'id1'},
                        'sentiment': {'S': 'positive'},
                        'message': {'S': 'Message 1'}
                    }
                }
            },
            {
                'PutRequest': {
                    'Item': {
                        'id': {'S': 'id2'},
                        'sentiment': {'S': 'negative'},
                        'message': {'S': 'Message 2'}
                    }
                }
            },
            {
                'DeleteRequest': {
                    'Key': {
                        'id': {'S': 'id_to_delete'},
                        'sentiment': {'S': 'sentiment_of_item_to_delete'}
                    }
                }
            }
        ]
    }
)

print(response)


response = dynamodb_client.batch_get_item(
    RequestItems={
        'mytable': {
            'Keys': [
                {
                    'id': {'S': 'id1'},
                    'sentiment': {'S': 'positive'}
                },
                {
                    'id': {'S': 'id2'},
                    'sentiment': {'S': 'negative'}
                }
            ],
            'ProjectionExpression': 'id, sentiment, message'
        }
    }
)

print(response['Responses']['mytable'])
