# zip code
```
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
```
zip dep.zip b.py
```
```
aws lambda create-function \
    --function-name genre_function \
    --runtime python3.11 \
    --zip-file fileb://dep.zip \
    --handler b.lambda_handler \
    --role 

```
* update the code
```
aws lambda update-function-configuration \
    --function-name genre_function \
    --tracing-config Mode=Active
```
# invoke lambda cli
```
aws lambda invoke \
    --function-name genre_function \
    --cli-binary-format raw-in-base64-out \
    --payload '{ "genre": "Action" }' \
    response.json
```
