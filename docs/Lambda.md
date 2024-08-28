# Events
## S3 notification trigger
* get key and bucket
```python
for record in event['Records']
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
```



# zip code
```python
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
import random

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("movies")
popular_movies = [
    {'year': 1997, 'title': "Titanic"},
    {'year': 2010, 'title': "Despicable Me"},
    {'year': 2013, 'title': "World War Z"},
    {'year': 2013, 'title': "Iron Man 3"}
]
for x in range(1, 201):

    table.get_item(Key=random.choice(popular_movies))

    if x%10 == 0:
        print(f"{x} reads complete")

    time.sleep(1)

```
```bash
zip dep.zip b.py
```
```bash
aws lambda create-function \
    --function-name genre_function \
    --runtime python3.11 \
    --zip-file fileb://dep.zip \
    --handler b.lambda_handler \
    --role 

```
* update the code
```bash
aws lambda update-function-configuration \
    --function-name genre_function \
    --tracing-config Mode=Active
```
# invoke lambda cli
```bash
aws lambda invoke \
    --function-name genre_function \
    --cli-binary-format raw-in-base64-out \
    --payload '{ "genre": "Action" }' \
    response.json
```
# SAM
```bash
sam init
sam build
```

```yaml
      Runtime: python3.8
      AutoPublishAlias: live
      DeploymentPreference:
        Type: Canary10Percent5Minutes #or Linear10PercentEvery1Minute
        
```