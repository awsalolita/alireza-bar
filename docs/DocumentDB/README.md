# Connecting 
### CommandLine
```bash
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
mongosh --tls --host $docDbClusterEndpoint:$docDbClusterEndpointPort \
--tlsCAFile rds-combined-ca-bundle.pem \
 --username $docDbUsername \
 --password $docDbPassword \
 --retryWrites=false
mongo --ssl --host mydocdb.cluster-cek2panatleb.us-west-2.docdb.amazonaws.com:27017 --sslCAFile global-bundle.pem --username docdbadmin --password <insertYourPassword>
```
### Python
```python

client = MongoClient('mongodb:///`<DBUsername>:<DBPassword>`
                    @`<DBCluster>`:27017/?tls=true&tlsCAFile=/home/ssm-user/
                    rds-combined-ca-bundle.pem&replicaSet=rs0')
```
```python
client = pymongo.MongoClient(
    cluster_uri,
    tls = True,
    retryWrites = False,
    tlsCAFile = '/opt/python/global-bundle.pem',
    username = secret_username,
    password = secret_password,
    authSource = 'admin',
    readPreference = 'secondaryPreferred',
    appName = 'productRecommendations'
)
```

# Commands
* Collection -> db
* 
```bash
show dbs;
use <db>;
show collections;

db.<collections>.findOne()
db.<collections>.find({"cast.name":"Sylvester Stallone"}).count()
```

```bash
resultCount = 0;
db.getCollectionNames().forEach(
  function(collection) {
    resultCount = resultCount + db[collection].find(
      {"cast.name": "Matt Damon"}).count()
    }
  );
print("Total Movies Played between 1990 to 2005: "+ resultCount);

db.reviews.createIndex({"customerId": 1},{"workers": 2})
```

# Example
* [find actor name](DocumentDBLookupActer.py)