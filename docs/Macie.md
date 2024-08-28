# Custom identifier
* in the documents

# python code to create a job

```python
macie_client = boto3.client('macie2')
def list_custom_data_identifiers():
    print('list_custom_data_identifiers')
    """Returns a list of all custom data identifier ids"""
    custom_data_identifiers = []
    try:
        response = macie_client.list_custom_data_identifiers()
        for item in response['items']:
            custom_data_identifiers.append(item['id'])
        return custom_data_identifiers
    except ClientError as e:
        logging.error(e)
        sys.exit(e)

def create_classification_job(data_bucket, account_id, custom_data_identifiers, file_name):
    print('create_classification_job')
    unique_id = "CheckData_" + file_name + str(int(time.time()))
    """Create 1x Macie classification job"""
    try:
        response = macie_client.create_classification_job(
            customDataIdentifierIds=custom_data_identifiers,
            description='Check new data (1x)',
            jobType='ONE_TIME',
            initialRun=True,
            clientToken=unique_id,
            name=unique_id,
            s3JobDefinition={
                'bucketDefinitions': [
                    {
                        'accountId': account_id,
                        'buckets': [
                            data_bucket
                        ]
                    }
                ],
                'scoping': {
                    'includes': {
                        'and': [
                            {
                                'simpleScopeTerm': {
                                    'comparator': 'STARTS_WITH',
                                    'key': 'OBJECT_KEY',
                                    'values': [
                                        file_name,
                                    ]
                                }
                            },
                        ]
                    }
                }
            }
        )
        #logging.debug(f'Response: {response}')
        return response
    except ClientError as e:
        logging.error(e)
        sys.exit(e)
```