```
yum install redis6
redis6-cli -h master.newcluster.4zxwf0.use1.cache.amazonaws.com --tls -a "xFc9^Pt$qvqapBxFc9^Pt$qvqapB"
```


```
keys *
zrangebyscore SensorData (1410000000000 14400000000000
hget DEVICE_ID temperature
zscan SensorData 0 MATCH 2* COUNT 100
hgetall DEVICE_ID
```

# memory db
```bash
aws memorydb create-user \
     --user-name actoruser \
     --access-string "on -actor:* +@all" \
--authentication-mode Passwords="MemoryDBActorUserl23",Type=password
```
```
./redis-cli -c -h clustercfg.sample-cluster.yoicyb.memorydb.us-east-1.amazonaws.com --tls -p 6379 --user movieuser --pass MemoryDBMovieUser123
```
* Under Access string, enter: on ~movie:* +@all in the text box. This will give movieuser access to all the movie: keys and movieuser can run all commands to these keys.

# python
```python
#!/usr/bin/env python3

# step 1: import the redis-py client package
import redis
from redis.cluster import RedisCluster as Redis

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "clustercfg.sample-cluster.yoicyb.memorydb.us-east-1.amazonaws.com"
redis_port = 6379
redis_user = "movieuser"
redis_password = "MemoryDBMovieUser123"

def hello_redis(event, context):
    """Example Hello Redis Program"""
# step 3: create the Redis Connection object
try:
    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8.  This is client specific.
    r = Redis(host=redis_host, port=redis_port, username=redis_user, password=redis_password, decode_responses=True,ssl=True, ssl_cert_reqs="none")
    # step 4: Set the hello message in Redis
    r.set("movie:002", "Hello Redis!!!")
    # step 5: Retrieve the hello message from Redis
    msg = r.get("movie:002")
    print(msg)
except Exception as e:
    print(e)
```