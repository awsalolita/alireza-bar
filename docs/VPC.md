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