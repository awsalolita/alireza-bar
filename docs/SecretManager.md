# Secretman Script
* my image `docker.io/arpjoker/awssecret`
```
touch test
docker run -e AWS_ACCESS_KEY_ID=AKIAQ3EGS4QEHXIY6S2X -e AWS_SECRET_ACCESS_KEY=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  -e AWS_REGION=us-east-1  -v ./test:/app/test arpjoker/awssecret python3 main.py  appconfig myapp:myenv:myconfig json test
```
* types are json , equal , yaml

# appconfig permissions
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Statement1",
			"Effect": "Allow",
			"Action": [
				"appconfig:GetConfiguration",
				"appconfig:StartConfigurationSession",
				"appconfig:GetLatestConfiguration"
			],
			"Resource": ["*"]
		}
	]
}
```

# eks
## AppConfig
* deployment is [here](./EKS/eks/Deployment/ServiceAccWithIAM_Deployment.yaml)
```yaml
containers:
  - name: appconfig-agent
    image: public.ecr.aws/aws-appconfig/aws-appconfig-agent:latest
    ports:
    - name: http
      containerPort: 2772
      protocol: TCP
    env:
    - name: us-east-1
      value: region
    imagePullPolicy: IfNotPresent
```

* `curl "http://localhost:2772/applications/myapp/environments/myenv/configurations/myconfig" > server.ini` in cmd too