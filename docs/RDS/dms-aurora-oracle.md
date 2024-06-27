* for multiple account , the other secret must use cutomer managed kms key

* aurora secret manager doesnt have host and port  , create one
* use another user , NOT ADMIN
* oracle table created will be under admin user like for person table:
ADMIN.PERSON


```
{
  "username": "NOTadmin",
  "password": "-1kHY[S{d-92HCRGrsY0En*DR7z-" ,
  "port": "1521",
  "host": "aurora-instance-1.cnski00mq9y2.us-east-1.rds.amazonaws.com"
}
```

* **dms.us-east-1.amazonaws.com** in trust entity
* policy of the role that dms uses to access another acc
```
{
"Version": "2012-10-17",
"Statement": [
{
"Action": [
"secretsmanager:GetSecretValue"
],
"Resource": "arn:aws:secretsmanager:<Region>:<AccountID A>:secret:secret_name",
"Effect": "Allow"
},
{
"Action": ["kms:Decrypt",
"kms:DescribeKey"],
"Resource": "arn:aws:kms:<Region>:<AccountID A>:key/xxxxxx",
"Effect": "Allow"
}
]
}
```

* other account secretmanager access policy

```
{
  "Version" : "2012-10-17",
  "Statement" : [ {
    "Effect" : "Allow",
    "Principal" : {
      "AWS" : ["arn:aws:iam::<ACC1NUMBER>:role/<ROLE>" ]
    },
    "Action" : [ "secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret" ],
    "Resource" : "KEYARN "
  }
  , {
    "Effect" : "Allow",
    "Principal" : {
      "AWS" : "arn:aws:iam::<ACC1NUMBER>:root"
    },
    "Action" : "secretsmanager:DescribeSecret",
    "Resource" : "*"
  },
  
{
"Effect" : "Allow",
"Principal" : {
"AWS" : [
"arn:aws:iam::<ACC1NUMBER>:role/<ROLE>",
"arn:aws:iam::<>ACC1NUMBER:role/admin"
]
},
"Action" : [ "secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret" ],
"Resource" : "*"
}
  ]
}
```

* kms access policy
```
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::<ACC1NUMBER>:role/admin",
                    "arn:aws:iam::<ACC1NUMBER>:role/<ROLE>"
                ]
            },
            "Action": [
                "kms:Decrypt",
                "kms:DescribeKey"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<ACC1NUMBER>:role/<ROLE>"
            },
            "Action": "kms:Decrypt",
            "Resource": "<KMSKEYARN>",
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": "secretsmanager.us-east-1.amazonaws.com"
                },
                "StringLike": {
                    "kms:EncryptionContext:SecretARN": "<SECRETARN>"
                }
            }
        }
```