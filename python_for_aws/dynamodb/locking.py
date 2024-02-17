
## IMPLEMENTING LOCKING IN DYNAMODB BY VERSION

import boto3

# Initialize a DynamoDB client
dynamodb_client = boto3.client('dynamodb')

# Define the table and user ID, along with the new email
table_name = 'Users'
user_id = 'user123'
new_email = 'newemail@example.com'
current_version = 1  # This is the version you've read from the item

try:
    # Update the user's email and increment the version atomically
    response = dynamodb_client.update_item(
        TableName=table_name,
        Key={'userId': {'S': user_id}},
        UpdateExpression='SET email = :email, version = version + :inc',
        ConditionExpression='version = :current_version',
        ExpressionAttributeValues={
            ':email': {'S': new_email},
            ':current_version': {'N': str(current_version)},
            ':inc': {'N': '1'}  # Increment the version by 1
        },
        ReturnValues='UPDATED_NEW'
    )

    # If the update succeeds, the new version number is included in the response
    print("Update succeeded:", response)

except dynamodb_client.exceptions.ConditionalCheckFailedException:
    # This exception is raised if the condition is not met, e.g., the version has changed
    print("Update failed: The item's version has changed since it was last read.")
