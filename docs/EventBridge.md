# Target Transformation
* `*` in the list
* 
# EventBridge on ec2:RunInstances
* api call is `RunInstances`
```json
{
  "source": ["aws.ec2"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["ec2.amazonaws.com"],
    "eventName": ["RunInstances"]
  }
}
```

# python put event
```python
client = boto3.client('events')
client.put_events(
      Entries=[
        {
          'DetailType': 'eventtype',
          'Detail': {...},
          'EventBusName': "lab_event_bus",
          'Source':"cook_pizza"
        },
      ]
    )
```

# Concept
* Buses
* Rules: event patterns from cloudtrail or other services
* target , can be api target , aws services , or another bus
* input transforamtion to transform the matched pattern
