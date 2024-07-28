# Iot core

* create a thing 
* make a rule for the thing
```sql
select * from 'mytopic'
```
* make a policy to allow *


# rule to kinesis data stream
* needs an iam role
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "kinesis:PutRecord",
                "kinesis:PutRecords"
            ],
            "Resource":"<StreamArn>" ,
            "Effect": "Allow"
        }
    ]
}
```
