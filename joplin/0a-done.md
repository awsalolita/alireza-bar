# Api Gateway
## Api keys
* limit clients request and such things
* in their `X-API-Key` header
* create key , then usage plan and associate it with the stage
```
curl -H "x-api-key: RyfN0rLsfl5Z0IFuijjzo5HAdtPWuaCBAjpZR5W9" https://il32676bwk.execute-api.us-east-1.amazonaws.com/test
```

# Cognito
* user pool 
	* for AUTHENTICATION
* get tokenid
```
aws cognito-idp initiate-auth --client-id 8039r1b0m7bnlh51eol5i1k2u --auth-flow USER_PASSWORD_AUTH  --auth-parameters USERNAME=arp.joker82@gmail.com,PASSWORD=12345678
```
* identity pool
	* temp access for aws credentials
		* for AUTHORIZATION
	* you can use identity pool to generate aws access token to use aws services
* role based  , assigning groups a specific role
	* `https://docs.aws.amazon.com/cognito/latest/developerguide/role-based-access-control.html#token-claims-for-role-based-access-control`

## JWT
* token id  contains `claims` of the user like user group
# SSH
## ssh ways
* ssm
* create endpoint
* user data
# Lambda
## with api gateway
* when you enabled lambda proxy integration
	* you get pathparameters and such
* but when you dont you only get the body that you send
* invoke another function

# Lambda
* testing in vpc , private and public
* api gateway to private lambda
### secret manager + parameter store
* lambda extention
* json.loads (the fucking s)
* codes are ready

# RDS
## DMS
* migration
* creating replication instances
* create subnet group
* searched for ways 
* homogeneous , wasnt it 
* bidirectional
	* 
* for rds replication it must have the required parameter group
	* log format

* exlude some tables , just testing , WORKS
* one table works
* one way works
	* just be careful about the tables you include and exlude
* two way
	* parameter group
	* aurora needs ROW as binlog_format

# ECS
* first we create task definition (you set the iam here)
* then we create a service in our cluster
* task execution role vs task role
	* execution role is for when 
		* pull image from ECR
		* send logs to CW
		* getting **secrets**
* **attaching efs**
		* **Enable DNS hostnames**
* efs override nginx default html
* cloudfront only to elb
# cloudfront
* restrict access to lambda with invoke permissions
* restrict access to ELB with
	* custom header from cloudfront and edit the rule on ELB
	* use https for origin request
	* limit acces by security group
* for s3 , s3 needs to be publicly accessible
* default object
# WAF
* integration with multiple apps
# offload authentication to elb
* elb to cognito
# database iam authentication
* needs ssl
* get ssl from global ...
* disables regular password  login for the user 
* for lambda usage you can put the ceritficates on s3 
# s3
* enabling server access logging
* aws cloudtrail dataevents 
# api gateway 
* private
* need vpc endpoint
* api key
* vpc link needs NLB
* in nlb untick the fucking inforce privatelink sg
* 