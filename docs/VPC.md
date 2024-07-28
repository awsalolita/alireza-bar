# Endpoint
* restrict with policy (takes time)
```
{
	"Statement": [
		{
			"Action": "execute-api:Invoke",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::774832926123:role/instance-role"
			},
			"Resource": "arn:aws:execute-api:us-west-2:774832926123:9lvbidevs1/*/GET/orders"
		}
	]
}

```
* restrict with security group

# FlowLogs
* create loggroup
* role to write to the loggroup
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ],
      "Resource": "*",
      "Effect": "Allow"
    }
  ]
}
```
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "vpc-flow-logs.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```