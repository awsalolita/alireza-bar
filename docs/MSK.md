# python code
* exactly like kafka
### Producer
```python

from kafka import KafkaProducer
import boto3
msk = boto3.client("kafka")
response = msk.get_bootstrap_brokers(
            ClusterArn=<cluster_arn>
        )
producer = KafkaProducer(security_protocol="PLAINTEXT",bootstrap_servers=response["BootstrapBrokerString"],value_serializer=lambda x: x.encode("utf-8"))
data = json.dumps({
        "ticker" : "x",
        "order_class" : "y"
    })
producer.send("stock_transactions", value=data)
```
