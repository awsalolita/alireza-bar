### imports
```python
import boto3
import json
import os

s3 = boto3.resource('s3')
mybucket = "mybucket"
```
### ReadObject Body
```python
obj = s3.Object(bucket_name , filename)
body = obj.get()['Body'].read().decode("utf-8")
```
### ReadObject Json
* [here](SelectObjectSql.py)
### ReadObject SQL CSV
```python
resp = s3.select_object_content(
    Bucket=bucketName,
    Key='TrafficEvents.csv', # Gzip file
    ExpressionType='SQL',
    Expression=(f"SELECT * from s3object s where s.\"zip code\" = '{zip}'"),
    InputSerialization = {'CSV': {"FileHeaderInfo": 'Use'}, 'CompressionType':'NONE'}, # GZIP
    OutputSerialization = {'CSV': {}},
)
```

### WriteObject Body
```python
# string or make csv file
line = s3object+','+row['Text']+','+row['Category']+','+row['Type']+','+str(row['Score'])
s3.put_object(Bucket=mybucket, Key="keyfilepath.csv", Body=line)
```
### Upload a directory
```python
def uploadDirectory(path,bucketname):
    for root,dirs,files in os.walk(path):
        for file in files:
            s3.upload_file(os.path.join(root,file),bucketname,file)
            
uploadDirectory('./directory' , mybucket)
```
### Presigned url
```python
url = boto3.client('s3').generate_presigned_url(
    ClientMethod='get_object', 
    Params={'Bucket': mybucket, 'Key': targetpath},
    ExpiresIn=3600)
```
### Lambda s3 trigger
```python

bucket = event['Records'][0]['s3']['bucket']['name']	
s3object = event['Records'][0]['s3']['object']['key']
```
