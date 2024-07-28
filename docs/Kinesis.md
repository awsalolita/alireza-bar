# Cloudwatch subscription filter to kinesis DataStreams
* you can provision only one shard


# gunzip the data from kinesis from cloudwatch
* test event
```json
{"Records": [{"kinesis": {"kinesisSchemaVersion": "1.0", "partitionKey": "e9239619b397ede01b2234e44776f191", "sequenceNumber": "49654139499842831375873712704771204015368165377871708162", "data": "H4sIAAAAAAAA/7WRTWsbMRCG/4qYUwtO0Gj0fTPEDRR6qXMLxqx3VVfgXS2S1q0J/u9lnaQkpL20BOYgxKuX5xk9QB9Kafbh7jQG8HCzvFtuv6zW6+XtChaQfgwhgwfUSJpzayQaWMAh7W9zmkbw0DW12TUlbEvIx5C3JbRTjvW0PaR9eYyuaw5NDx7iFec76oLqlLWGlNAcFlCmXWlzHGtMw6d4qCEX8Pe/i9ljMSvlO2vTMIR2DrJL/ebSvzqGoc5vHiB24IEsOTKoUBnHDZF0ZEmhEIKs5Zakc8qR5FahVMIIdNYoK2eWGvtQatOP4NEI1ESGuHV68bwm8PB5OjAhGDeelCfO4niF/HkQZ9DuXnGt1Mazr6EN8Rg61sXyRM++5dQz5NfzXDtkY8qVSSWc9oj+RTJ0bHdiUwkZzov/k8P3kLt5SXqxmllZqVMXhvpnxbcmQiuOxqJEoa0jyxWRtsYpJaXSjqxy0kouJVkk6/72TUo79y8mEjeejU2/nYb488N860soJabho2dPJ9YeUpkdU36lCOfN+Rcm2lbgQgMAAA==", "approximateArrivalTimestamp": 1721633736.064}, "eventSource": "aws:kinesis", "eventVersion": "1.0", "eventID": "shardId-000000000000:49654139499842831375873712704771204015368165377871708162", "eventName": "aws:kinesis:record", "invokeIdentityArn": "arn:aws:iam::161360087417:role/LambdaCWLogsProcessorRole", "awsRegion": "us-east-1", "eventSourceARN": "arn:aws:kinesis:us-east-1:161360087417:stream/security_log_stream"}]}
```

```python3
str(gzip.decompress(base64.b64decode(a)).decode())
```

# apache flink notebook
* creating notebook
* creating glue db
* create table from kinesis data stream

* ec2 cwagent logs for ssh
```sql
%flink.ssql

DROP TABLE IF EXISTS security_logs;
CREATE TABLE security_logs (
  `messageType` STRING,
  `owner` STRING,
  `logGroup` STRING,
  `logStream` STRING,
  `subscriptionFilters` STRING,
  `id` STRING,
  `dateTime` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `message` STRING
  )
WITH (
  'connector' = 'kinesis',
  'stream' = 'processed_security_logs',
  'aws.region' = 'AWS_REGION',
  'scan.stream.initpos' = 'TRIM_HORIZON',
  'format' = 'json'
);

```
# apache flink application
* needs a jar application
* s3 and log permissions














# Lab , lambda kinesis to apache link
* security logs from /var/log/security to kinesis then to lambda to be processed 
```python
import json
import base64
import boto3
import os
import gzip

kinesis_client = boto3.client('kinesis')
KINESIS_DATA_STREAM = os.environ['KinesisDataStream']

def lambda_handler(event, context):
  ### Get CloudWatch Logs records and decode them
  for record in event["Records"]:
    # Set partition key
    pk = str("PartitionKey1")
    # Print partition key to logs for verification and troubleshooting
    print("Partition key: " + str(pk))
    # Decode the log files data from CloudWatch Logs
    payload = base64.b64decode(record["kinesis"]["data"])
    # Print the decoded data to logs for verification and troubleshooting
    print("Decoded payload: " + str(payload))
    # CloudWatch Logs data is delivered in a compressed format and must be decompressed
    message = gzip.decompress(payload)
    # Print decompressed data to logs for verification and troubleshooting
    print("Uncompressed message: " + str(message))

  ### Extract JSON data
  # Load data from CloudWatch logs into memory
  event_data = json.loads(message)
  # Print to logs for verification and troubleshooting
  print("eventData JSON string: " + str(event_data))

  # Extract all top-level and nested keys, then recombine into a single string
  index1 = 0
  top_level_keys = ''
  # Loop to extract the top-level keys
  for key, value in event_data.items():
    index1 += 1
    if key != 'logEvents':
      if index1 < (len(event_data.keys())):
        top_level_keys += f'"{key}": "{value}", '
      else:
        top_level_keys += f'"{key}": "{value}"'
    if key == 'logEvents':
      # Loop to extract the nested keys in the logEvents
      for events in value:
        index2 = 0
        logEvents_keys = ''
        for logEvents_key, logEvents_value in events.items():
          index2 += 1
          if index2 < (len(events.keys())):
            logEvents_keys += f'"{logEvents_key}": "{logEvents_value}", '
          else:
            logEvents_keys += f'"{logEvents_key}": "{logEvents_value}"'
        # Print strings derived from each level of keys and values to validate the for loops are working correctly
        print(f'Top level keys: {top_level_keys}\n')
        print(f'Keys in logEvents: {logEvents_keys}\n')
        # Recombine the extracted top-level and nested keys to create a single string of keys and values
        recombined_message = f'{{{top_level_keys}{logEvents_keys}}}'
        # Convert the combined message string to a dict type
        convert_message_to_dict = json.loads(recombined_message)
        # Print the combined message data to logs for verification and troubleshooting
        print(f'Recombined message: {convert_message_to_dict}')
        # Encode the combined message data into a byte format required for the Kinesis data stream
        encoded_message = json.dumps(convert_message_to_dict, indent=2).encode('utf-8')
        # Print the encoded message data to logs for verification and troubleshooting
        print("Encoded message: " + str(encoded_message))
        # Send encoded extracted data to a Kinesis data stream
        response = kinesis_client.put_record(Data=encoded_message, PartitionKey=pk, StreamName=KINESIS_DATA_STREAM)
        # Print the response from Kinesis to logs for verification and troubleshooting
        print(response)

```
* vpc logs lambda processor
```python
import json
import base64
import boto3
import os
import gzip

kinesis_client = boto3.client('kinesis')
KINESIS_DATA_STREAM = os.environ['KinesisDataStream']

def lambda_handler(event, context):
  ### Get CloudWatch Logs records and decode them
  for record in event["Records"]:
    # Set partition key
    pk = str("PartitionKey1")
    # Print partition key to logs for verification and troubleshooting
    print("Partition key: " + str(pk))
    # Decode the log files data from CloudWatch Logs
    payload = base64.b64decode(record["kinesis"]["data"])
    # Print the decoded data to logs for verification and troubleshooting
    print("Decoded payload: " + str(payload))
    # CloudWatch Logs data is delivered in a compressed format and must be decompressed
    message = gzip.decompress(payload)
    # Print decompressed data to logs for verification and troubleshooting
    print("Uncompressed message: " + str(message))

  ### Extract JSON data
  # Load data from CloudWatch logs into memory
  event_data = json.loads(message)
  # Print to logs for verification and troubleshooting
  print("eventData JSON string: " + str(event_data))

  # Extract all top-level and nested keys, then recombine into a single string
  index1 = 0
  top_level_keys = ''
  # Loop to extract the top-level keys
  for key, value in event_data.items():
    index1 += 1
    if key != 'logEvents':
      if index1 < (len(event_data.keys())):
        top_level_keys += f'"{key}": "{value}", '
      else:
        top_level_keys += f'"{key}": "{value}"'
    if key == 'logEvents':
      # Loop to extract the nested keys in the logEvents key
      for events in value:
        index2 = 0
        logEvents_keys = ''
        extractedFields_keys = ''
        for logEvents_key, logEvents_value in events.items():
          index2 += 1
          index3 = 0
          if logEvents_key != 'extractedFields':
            if index2 < (len(events.keys())):
              logEvents_keys += f'"{logEvents_key}": "{logEvents_value}", '
            else:
              logEvents_keys += f'"{logEvents_key}": "{logEvents_value}"'
          elif logEvents_key == 'extractedFields':
            # Loop to extract the nested keys in the extractedFields key
            for extractedFields_key, extractedFields_value in logEvents_value.items():
              index3 += 1
              if index3 < (len(logEvents_value.keys())):
                extractedFields_keys += f'"{extractedFields_key}": "{extractedFields_value}", '
              else:
                extractedFields_keys += f'"{extractedFields_key}": "{extractedFields_value}"'
        # Print strings derived from each level of keys and values to validate the for loops are working correctly
        print(f'Top level keys: {top_level_keys}\n')
        print(f'Keys in logEvents: {logEvents_keys}\n')
        print(f'Keys in extractedFields: {logEvents_keys}\n')
        # Recombine the extracted top-level and nested keys to create a single string of keys and values
        recombined_message = f'{{{top_level_keys}{logEvents_keys}{extractedFields_keys}}}'
        # Convert the combined message string to a dict type
        convert_message_to_dict = json.loads(recombined_message)
        # Print the combined message data to logs for verification and troubleshooting
        print(f'Recombined message: {convert_message_to_dict}')
        # Encode the combined message data into a byte format required for the Kinesis data stream
        encoded_message = json.dumps(convert_message_to_dict, indent=2).encode('utf-8')
        # Print the encoded message data to logs for verification and troubleshooting
        print("Encoded message: " + str(encoded_message))
        # Send encoded extracted data to a Kinesis data stream
        response = kinesis_client.put_record(Data=encoded_message, PartitionKey=pk, StreamName=KINESIS_DATA_STREAM)
        # Print the response from Kinesis to logs for verification and troubleshooting
        print(response)

```
```sql
%flink.ssql

DROP TABLE IF EXISTS security_logs;
CREATE TABLE security_logs (
  `messageType` STRING,
  `owner` STRING,
  `logGroup` STRING,
  `logStream` STRING,
  `subscriptionFilters` STRING,
  `id` STRING,
  `dateTime` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `message` STRING
  )
WITH (
  'connector' = 'kinesis',
  'stream' = 'processed_security_logs',
  'aws.region' = 'AWS_REGION',
  'scan.stream.initpos' = 'TRIM_HORIZON',
  'format' = 'json'
);
##########
%flink.ssql

DROP TABLE IF EXISTS vpc_flow_logs;
CREATE TABLE vpc_flow_logs (
  `messageType` STRING,
  `owner` STRING,
  `logGroup` STRING,
  `logStream` STRING,
  `subscriptionFilters` STRING,
  `id` STRING,
  `dateTime` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `message` STRING,
  `action` STRING,
  `srcaddr` STRING,
  `srcport` INTEGER,
  `dstaddr` STRING,
  `dstport` INTEGER,
  `interface_id` STRING,
  `subnet_id` STRING,
  `protocol` INTEGER,
  `flow_direction` STRING,
  `account_id` STRING
  )
WITH (
  'connector' = 'kinesis',
  'stream' = 'processed_vpc_flow_logs',
  'aws.region' = 'AWS_REGION',
  'scan.stream.initpos' = 'TRIM_HORIZON',
  'format' = 'json'
);
########
%flink.ssql

SELECT * FROM vpc_flow_logs;

```