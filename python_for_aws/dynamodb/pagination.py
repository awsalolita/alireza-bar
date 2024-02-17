import boto3

# Initialize a DynamoDB client
dynamodb_client = boto3.client('dynamodb')

# Define the table and the post ID you're interested in
table_name = 'Posts'
post_id = 'specific_post_id'

# Initialize the empty list to store all comments
all_comments = []

# Initialize the pagination key
last_evaluated_key = None

# Loop to handle pagination
while True:
    if last_evaluated_key:
        response = dynamodb_client.query(
            TableName=table_name,
            KeyConditionExpression='postId = :postId',
            ExpressionAttributeValues={
                ':postId': {'S': post_id}
            },
            ExclusiveStartKey=last_evaluated_key
        )
    else:
        response = dynamodb_client.query(
            TableName=table_name,
            KeyConditionExpression='postId = :postId',
            ExpressionAttributeValues={
                ':postId': {'S': post_id}
            }
        )
    
    # Add the current batch of items to the all_comments list
    all_comments.extend(response.get('Items', []))
    
    # Check if there are more items to fetch
    last_evaluated_key = response.get('LastEvaluatedKey')
    if not last_evaluated_key:
        break

# Now, all_comments contains all comments for the specified post
print(all_comments)
