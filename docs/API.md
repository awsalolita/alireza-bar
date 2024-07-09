* api key
```
curl -H "x-api-key: AQiTWLjMXvS4MRboF4Kp7N7VxrGjOYgi"
```

restrict
* resource policy example
* can enable iam as well
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:*:*:*",
      "Condition": {
        "IpAddress": {
          "aws:VpcSourceIp": "10.199.0.0/24"
        }
      }
    },
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:*:*:*",
      "Condition": {
        "StringNotEquals": {
          "aws:sourceVpc": "vpc-03fb377a4f7684f0c"
        }
      }
    }
  ]
}
```