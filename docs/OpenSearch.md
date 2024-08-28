# Index types
* The index format is `name/type` 
* list of mapping tuples, each consisting of: ` (source column, source type, target column, target type)`
# python code
* putting logs
```python
from requests_aws4auth import AWS4Auth
import boto3,logging
import json
service = 'es'
credentials = boto3.Session().get_credentials()
dynamodb_client = boto3.client('dynamodb')
session = boto3.session.Session()
region = session.region_name
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
host = "https://search-vital-signs0-hsf6zrvugjdbmxfxnpblda3l44.us-east-1.es.amazonaws.com"
index = os.environ['OPENSEARCH_INDEX']
datatype = '_doc'
url = host + '/' + index + '/' + datatype + '/'
headers = { "Content-Type": "application/json" }
## Create the JSON document that will be sent to OpenSearch
document = { 
    "id": id, 
    "date_time": json_data['data']['date_time'],
    "monitor_id": json_data['data']['monitor_id'],
    "heart_rate": json_data['data']['heart_rate'],
    "systolic_blood_pressure": json_data['data']['systolic_blood_pressure'],
    "diastolic_blood_pressure": json_data['data']['diastolic_blood_pressure'],
    "blood_oxygen_level": json_data['data']['blood_oxygen_level'],
    "body_temperature": json_data['data']['body_temperature'],

}

logger.info(json.dumps(document, indent=2))
r = requests.put(url + id, auth=awsauth, json=document, headers=headers)
```


# Insert, Update, Delete based on dynamodb trigger
```python
service = 'es'
credentials = boto3.Session().get_credentials()
dynamodb_client = boto3.client('dynamodb')
session = boto3.session.Session()
region = session.region_name
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
for record in event['Records']:
    try:
        eventName = record['eventName']
        # PUT sample-index/_doc/1
        if eventName == 'INSERT':
            document =  (record['dynamodb']['NewImage'])
            id = document['id']
            url = host + '/' + index + '/' + '_doc' + '/' + id
            responsedata = requests.put(url + id, auth=awsauth, json=document, headers=headers)
        # POST /sample-index1/_update/1
        if eventName == 'MODIFY':
            document = dynamo_obj_to_python_obj(record['dynamodb']['NewImage'])
            id = document['id']
            url = host + '/' + index + '/' + '_update' + '/' + id
            new_document = {"doc":document}
            responsedata = requests.post(url + id, auth=awsauth, json=new_document, headers=headers)
        # DELETE /sample-index1/_doc/1
        elif eventName == 'REMOVE':
            document = dynamo_obj_to_python_obj(record['dynamodb']['OldImage'])
            id = document['id']
            url = host + '/' + index + '/' + '_doc' + '/' + id
            responsedata = requests.delete(url + id, auth=awsauth, json=document, headers=headers)
```