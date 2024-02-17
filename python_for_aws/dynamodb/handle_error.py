import boto3
import time
import random

# Initialize a DynamoDB client
dynamodb_client = boto3.client('dynamodb')

# Define the table name and item to be written
table_name = 'YourTableName'
item = {
    'PrimaryKey': {'S': 'yourPrimaryKeyValue'},
    'Attribute': {'S': 'yourAttributeValue'}
}

def write_with_retry(table_name, item, max_attempts=5):
    attempt = 0
    while attempt < max_attempts:
        try:
            dynamodb_client.put_item(TableName=table_name, Item=item)
            print("Item written successfully.")
            return
        except dynamodb_client.exceptions.ProvisionedThroughputExceededException:
            print("Write throttled, will retry...")
            # Exponential backoff with jitter
            time.sleep((2 ** attempt) + (random.randint(0, 1000) / 1000))
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            break
        attempt += 1

    print("Failed to write item after retrying.")

# Attempt to write the item with retry logic
write_with_retry(table_name, item)
