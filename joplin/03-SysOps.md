# Deployment
* SAN storage -> io2 Block express
* 5xx vs 4xx errors
	* 502 bad gateway
	* 503 unavailable
	* 408 timeout client
	* 400 bad request
	* 464 incompatible protocol

* you can send logs of ELB to s3
* cant have public ip in ELB
* image builder
	* pipelines
	* needs ssm permission to run stuff and can be deleted after
	* can build docker image
	* test components , build components
	* create infrastructure for builfing image

* cloudFormation
	* roll back fail
		* you changed something manually
	* stackset
		* run single cloudformation in multiple accounts
		* need cross acount roles 
		* RAM

* Canary , rolling , blue/green updates
* PatchManager
	* compliance and shit
* Run command
	* gives you the cli 

* OpsWork -> configuration management , CaC
	* Puppet , chef 
### Questions
* ELB access logs contains  detailed information relating to incoming requests to your Elastic Load Balancer not cloudwatch
*  ELB access logs is not enabled by **default** , **its encrypted by default in s3**

* 20,000 IOP -> iops provisioned
* UnHealthyHostCount

# Monitoring

* what can cloudwatch monitor
	* EC2
		* cpu , network , disk (NOT MEMORY , OS logs(agent) , )
		* 5 min intervals by default
	* auto scaling
	* ELB
	* route 53
	* Lambda
	* EBs
	* storage gateway
	* Cloudfront
	* dynamo , elasticache , RDS , redshift , EMR , SNS , SQS

* widgets 

* CloudWatch Logs
	* components for EC2
		* cloudwatch agent , role for CW , rsyslog , StateD daemon ,  
	* realtime
	* retention from 1 day to 10 years

* Metric Filter
	* namespace
	* metric name and value

* SNS
	* limit of Quotas 
	* Health Events (event bridge)

* CloudTrail 
	* by default 90 Days , for indefinite storing you can store logs in s3
	* 5-15 minutes to get published in cloudtrail

* Config : conmpliance or not 
	* contains change history
	* create Rule to check for shit  
	* aws config it creates a S3 for itself the first time
	* manual evalution or scheduled 

* ssm
	* some predefined actions
	* Aws config can use some of this actions for remediation

 * Event Bridge
	 * Rules and targets(SNS)
	 * can be scheduled as well
	 * event bridge = cloud watch events

### Questions
* memory usage isnt sent to aws
* ec2 instances send data to CW at 5 mins interval , for 1 minute you will need to enable detailed monitoring

# Storage

* S3
	* o bytes files to 5 TB
	* make public
		* acl + make public
		* do not block public + bucket policy
	* MFA delete (versioning enabled)
	* allow access from some ip addresses -> bucket policy (condition)
	* S3 inventory
		* metadata 
		* report about objects
		* csv and apache* ...
		* daily weekly


* EFS
	* cannot be encrypted after creation
	* types (like s3)
	* burst to 100 MiB
	* burst , provisioned
	* kms for at rest

* athena 
	* needs s3 to store

* OpenSearch : elastic search
	* master and data nodes
	* multi/one AZ
	* **makie public or private only in creation , cannot change later**

* Storage Gateway
	* on premises appliance , hybrid
	* types
		* File gateway
			* S3 , nfs , 
		* FSx gateway
			* FSx
		* Volume gateway
			* stored mode
				* store backup in aws (ebs snapshot)
			* Cached mode
		* Tape gateway

* AWS backup
	* backup vault -> container of backups


# Reliability

* elastic -> scale with demand
* scalibilty -> big , small

* AWS Auto Scaling -> for more services
	* through tags , cloudformation scripting , or ec2 ASG 
	* plans
	* strategy
		* predictive
		* dynamic
	* for cost optimization

* Aurora
	* cluster volumes
	* storage auto scaling
	* self - repairing
	* two copies of data in  3 AZ 

* Aurora AutoScaling
	* add or remove replicas based on metric
	* Mysql and Postgres engine only
	* components
		* Auto scaling policy
		* auto scaling decisions
		* Target Values
			* CPU util
			* connections of replica
			* to maximum of 15 instances
				* oracle and sql server to 5 instances

* Multi AZ RDS
	* only for disaster recovery
	* backup and restores from secondary instances

* RDS Read replica
	* read load
	* auroradb has differences from others in replication
	* how 
		* a snapshot is created (if multi AZ , the snapshot is taken from secondary)
	* its only **Asynchronous** only
	* snapshots cannot be created from read replica
	* LAG REPLICA

* RDS snapshot
	* enable encryption for RDS
	* while sharing snapshots , you must share the key (not the default one)

* Multi AZ RDS
	* automatic failover even when single instance

* Elastic IP
	* static ip
	* 5 ip per region

* RPO - > how frequently you backup , how much can it lose
* RTO - > how long is the app gonna be down

* Service Maintenance Window
	* RDS
	* ElastiCache
	* Redshift
	* Neptune
	* DocumentDB

* EBS lifecycle policy
	* for ebs snapshot

* DynamoDB Stream for replica
	* stream of data  -> shards 
	* stored for 24h
	* View types 
	* create replica
	
### Questions
* **The Classic Load Balancer metric SurgeQueueLength measures the total number of requests queued by your Classic Load Balancer. An increased maximum statistic for SurgeQueueLength indicates that backend systems aren't able to process incoming requests as fast as the requests are received. When requests exceed the maximum SurgeQueueLength, the SpilloverCount metric starts to measure rejected requests. The maximum SurgeQueueLength is 1024.**

* **Increasing the value of the memcached_connections_overhead parameter will reduce the amount of memory available for storing items and provide a larger buffer for connection overhead, according to the AWS Elasticache documentation**

* modify the type of EBS volume without needing to snapshot the volume
* Memcache can have up to 40 nodes
* metrics -> **UnHealthyHostCount** not UnHealthyInstanceCount


# Security
* Amplification / Reflection attack
	* spoofed source ip (victims ip)

* slowloris
	* doesnt close connection

* AWS Shield 
	* protects , ELB , CloudFront , route 53
	* protects from ddos , floods , Reflection attack , layer 3-4 attacks

* IAM Identity center
	* single sign on

* IAM access Analyzer
	* resources that are shared external entity

* AWS Inspector vs Advisor
	* Advisor looks for optimization , **service quota** , fault tolerance , security -> for snapshots and bucket policy , SG 
	* Inspector

* AWS Org
	* service control policy 

* SCP -> service control policy

* AWS Tower
	* Landing zone
		*  default config for accounts
		*  Shared services , Log Archive , Security
	*  account factory
		*  account templates
	*  Guardrails
		*   Rules for governance 
		*   preventive
		*   Detective

* STS
	* component	: token , access key id , secret access key
	* identity broker capture username password

* KMS
	* CMK
		* encrypt and decrypt data
	* kms or custom that are created in cloudHSM


* dedicated instance vs dedicated host
	* dedicated host is the entire server 

* SSM parameter store vs SM(secret manager)
	* ssm doesnt have password generator but its free , no cross account and no rotation

* cloudTrail
	* only user with the kms key can access
	* data integrity with SHA-256
	* digest files signed by aws
	* dedicated s3

* Security Hub
	* enable resource recording in aws config
	* which standards do you want to apply
	* integrations

* GuardDuty
	* uses ML to detect threats
	* alerts
	* malicious domains and ips
	* analyze logs
	* 7-14 days of analyz at first
	* findings sent to event

* Secrets manager
	* username and password of the DB's
	* encrypted by kms
	* lambda function to rotate password
### Questions
* IAM credential report , csv file -> mfa_enabled
* You can create an IAM policy to enforce MFA sign-in
* memCache doesnt have native encryption for data at rest
* STS uses Active Directory Federation , Cross-Account Access , and Federation with Web Identity Providers
* AWS CloudFormation natively supports the Systems Manager Parameter Store
* penetration test May be performed by the customer against their own AWS infrastructure without prior authorization from AWS, as long as they're from the permitted services list


# Networking

* Nat Gateway
	* in public subnet , EIP
	* add to routetable of the private subnet

* when you create new NACL in vpc , it denies all
	* but the default NACL allows all
	* ethemeral ports

* Session Manager
	* CW logging  can be enabled

* VPC Endpoint
	* access other aws resources in aws backbone internet

* VPN 
	* ipsec encryption
	* virtual private gateway

* Direct connect
	* dedicated direct network connection 

* VPC Flow Logs
	* logs of the network
	* at subnet , vpc , interface level
![b2bf57fa90403f417857509c70041b03.png](../_resources/b2bf57fa90403f417857509c70041b03.png)

* route53
	* zone Apex (www.exm.com) can be used in alias but not in cname 

* Route53 resolver
	* dns queries from aws services

* CloudFront
	* TTL is 1 day by default
	* Distribution
	* invalidation

* Only CloudFront to s3
	* block public access to s3 and update s3 bucket policy
	* create origin access (OAI)

* logging of CF to s3
	* edge location is shown

* serve different versions with CF
	* create origin request policy
	* cookie
	* header
	* how to make cache hit ratio better (different headers result in cache miss)
		* only forward specific cookies not jibberish
		* the same for headers

* create alias of CF in route53
* custom cert for you to add domain in CF 


### Questions
* main table will apply to without explicit association
* What is a primary function of Route 53 Resolver?
	* Resolving DNS queries for resources in your VPC.
	* Resolving DNS queries for resources in your VPC and performing recursive lookups against public name servers for resources outside your VPC.
* OAI -> special CloudFront user
* alias vs cname


# Cost
* tags
* Cost Explorer
	* reports
	* activate aws tags for cost

* Cost Budgets
	* cost , usage , savings plans , Reservation
	* Alerts
	* Steps
		* enable recieve billing alerts
		* templates
		* billing alarms in CW

* Compute Optimizer
	* use ML
	* utilization data
	* optimization
	* exported to s3 in json or csv

* S3 Transfer acceleration
	* fast over long distances 
	* uses CF edge locations
	* the customer uploads to edge location

* S3 multipart upload
	* put object is 5gib but objects can be up to 5 TiB
	* recommended for over 100mb files
	* requiered for files over 5 GB 

* Placements
	* Cluster
		* Single AZ
	* Partition
		* seperated rack
		* logical segments
	* Spread
		* seperated rack

* Trusted advisor
	* uderutilized

* RDS proxy
	* idle connections and failover
* RDS Insights
	* waits , sql , host ,users
	*  


* Instance store
	* up to 10 GiB
	* 
### Questions
* dissallocating EIP isnt enough , delete them
* DynamoDB has no dedicated infrastructure footprint, and its cost is based on usage, performance, and storage