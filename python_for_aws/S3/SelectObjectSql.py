import boto3
s3 = boto3.client('s3')

zip = 98101 
bucketName = "mybucket"

resp = s3.select_object_content(
    Bucket=bucketName,
    Key='TrafficEvents.csv', # Gzip file
    ExpressionType='SQL',
    Expression=(f"SELECT * from s3object s where s.\"zip code\" = '{zip}'"),
    InputSerialization = {'CSV': {"FileHeaderInfo": 'Use'}, 'CompressionType':'NONE'}, # GZIP
    OutputSerialization = {'CSV': {}},
)
for event in resp['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        print("Stats details bytesScanned: ")
        print(statsDetails['BytesScanned'])
        print("Stats details bytesProcessed: ")
        print(statsDetails['BytesProcessed'])