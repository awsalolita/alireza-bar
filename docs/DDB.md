# PartiQL
```sql
INSERT INTO user_profiles VALUE 
{  
    'event_id': 'Winter12022',
    'user_id': 'ui101',
    'first_name' : 'John',
    'email': 'alireza.pourchali@gmail.com', --A valid email id to receive email that has been verified in Pinpoint
    'language' : 'en',
    'phone': '+12569527893', --Use your phone number to receive the voice prompt
    'preference': 'email',
    'phoneme': 'en-US'
}
```

# DAX 
* cache solution for ddb
* ports `8111` for unencrypted , `9111` for encrypted

```python
from boto3 import client, resource

db_source = "daxs://bankingappcluster.xys47s.dax-clusters.us-east-1.amazonaws.com" # OR 'dynamodb'

if (db_source != None and "dax" in db_source):
    client = AmazonDaxClient(endpoint_url=db_source)
    resource = AmazonDaxClient.resource(endpoint_url=db_source)
else:
    client = client(db_source)
    resource = resource(db_source)
mytable = resource.Table('mytable')
```