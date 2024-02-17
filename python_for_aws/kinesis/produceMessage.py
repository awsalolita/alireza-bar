import boto3
import json

# Initialize a boto3 client
kinesis_client = boto3.client('kinesis', region_name='YOUR_AWS_REGION')

def put_record_to_stream(data, stream_name):
    try:
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey='partition_key'  # Use a relevant partition key for your data
        )
        print(f"Record sent to Kinesis: {response}")
    except Exception as e:
        print(f"Error sending record to Kinesis: {e}")

if __name__ == '__main__':
    stream_name = 'YOUR_STREAM_NAME'
    
    # Example data to send
    data = {
        'message': 'Hello, Kinesis!',
        'timestamp': '2023-04-01T12:00:00Z'
    }

    # Send data to Kinesis Data Stream
    put_record_to_stream(data, stream_name)
