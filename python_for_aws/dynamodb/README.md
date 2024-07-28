# client vs resource

* user deserializer and serializer
* resource has better output

# on demand to provisioned
* changing once per 24 hours
```

``` 

# autoscaling
* for READ CAPACITY
```python
table_name = 'mytable'

def register_auto_scale_target_read():     
    aaClient.register_scalable_target(
        ServiceNamespace = 'dynamodb',
        ResourceId = "table/{}".format(table_name),
        ScalableDimension = "dynamodb:table:ReadCapacityUnits",
        MinCapacity = 1,
        MaxCapacity = 40)
        
#Create a scaling policy for Read capacity
def put_auto_scale_policy_read():
    aaClient.put_scaling_policy(
        PolicyName=policy_name,
        ServiceNamespace='dynamodb',
        ResourceId = "table/{}".format(table_name),
        ScalableDimension = "dynamodb:table:ReadCapacityUnits",
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': 70.0,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'DynamoDBReadCapacityUtilization'
            },            
        'ScaleOutCooldown': 60,
        'ScaleInCooldown': 60
        })  
```
* for write capacity
```python
#Define the scalable target for Write capacity
def register_auto_scale_target_write():     
    aaClient.register_scalable_target(
        ServiceNamespace = 'dynamodb',
        ResourceId = "table/{}".format(table_name),
        ScalableDimension = "dynamodb:table:WriteCapacityUnits", 
        MinCapacity = 1,
        MaxCapacity = 40000)
        
#Create a scaling policy for write capacity
def put_auto_scale_policy_write():
    aaClient.put_scaling_policy(
        PolicyName=policy_name,
        ServiceNamespace='dynamodb',
        ResourceId = "table/{}".format(table_name),
        ScalableDimension = "dynamodb:table:WriteCapacityUnits",
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': 70.0,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'DynamoDBWriteCapacityUtilization'
            },            
        'ScaleOutCooldown': 60,
        'ScaleInCooldown': 60
        }) 
```