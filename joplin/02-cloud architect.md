# chapter 01
*  aurora is compatible with mysql
* ami is template 


# IAM 
* attach policy to user , group , roles 
* you can change password policy (contians capital letters)
* IAM federation , identity federation , SAML -> Active directory

* trust policy 
	* **assume a role based on the user that is trusted in a role**

* EAR 
	* effect
	* action
	* resource

# S3
```
URL : https://<bucket>.s3.<region>.amazonaws.com/<object-key>
```
value , metadata , versionID

files to 5TB 

can host static content (index.html)

MFA for deleting
* versioning
	* previous versions do not get public
	* delete marker 
	* versioning cannot be delete

* standard : frequent rapid access , no cost for access ,website and gaming app  , big data analytics
* intelligent : no cost for access
* standard-IA : Rapid access less frequent , you pay to access data , backup for disaster recovery -> one zone 

* glacier: archive , cheap , pay when you access 
	*  instant retrieval 
	* flexible : retrieve in minutes up to 12 h
	* deep archive 

* ACL for obj , bucket policy for all
* lifecycle

* object lock : WORM write once read many
	* governance mode : some users with permission
	* compliance mode : no user can delete object 
	* glacier vault lock : enforce compliance controls over s3 glacier 
* retention
* legal hold

* Encryption
	* transit : tls/ssl
	* rest : SSE-s3 server side , SSE-KMS , SSE-C customer
		* remember kms has limits for reequest range  and kms limit cannot be changed 
	* enforce the encryption : put in header 

* more prefix more number of request that can be handled
* mulitpart upload , byte range download 	
* replication : delete markers dont get replicated by default , versioning is a must , existing object dont get repl automatically


#### questions 
* s3 can store 0 Byte!


# EC2

* fdafd

* reserved only region

* roles can be assumed

* magic ip address for getting metadata 
	* 169.254.169.254
	* apipa ip address 

* networking
	* ENI > VF
	* EN : 10Gbps - 100 , higher i/o
	* EFA
		* ML , HPC 

* placement
	* cluster: same AZ , low latency
	* spread : individual
	* partition : same rack

* **dedicated** 
	* **compliance**
	* **licensing**
	* on demand 
	* reserved 

* spot
	* fault tolerant , stateless
	* high performance computing
	* it goes over the price u mention 2 mins to delete
	* you have to delete your spot request (its different from terminating instances)

* spot fleet strategies  (can have on demand )
	* pools and strategies 

### question and labs
* when creating role from console for ec2 , it creates instance profile as well to attach to ec2  , in command line it doesnt 
	

# EBS , EFS
iops : read write  low-latency 
throughput: bit-per-sec large-dataset 
* types:
	* gp2-3: os boot volume
	* io1 : most expensive
	* io2 : same price as io1
	* st1 : low cost hdd , bigdata , cant be boot volume
	* sc1: lowest option

* migrate to another region
	* create snapshot 
	* copy snapshot to another region 
	* create volume/ami from snapshot  
* snapshots are incremental in nature

* encrypt an unencrypted
	* snapshot
	* copy snapshot and encrypt
	* create ami

* hibernation : save ram on disk

* efs: shared fs
	* 1000 concurrent
	* pay per use
	* types and lifecycles
		* standard
		* IA
	* change security group in network tab	

* FSx : windows
	* lustre : writes to s3

####question and labs
persist in fstab
```
fs-04f13b5459de97f01.efs.us-east-1.amazonaws.com:/		nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport 0 0
```

# databases

* RDS
	* OLTP : processes data from transactions in real time 
	* OLAP : process complex queries 
	* RDS not good for analyzing data (OLAP , redshift is good)
	* secondary doesnt work when primary is active (multi AZ cluster supports that )
	* read replica can be promoted and created whenever 
	* 

* Aurora 
	* postgres - mysql compatible 
	* 2 copies in 3 AZ = 6
	* 15 read replica (other 5)
	* automated failover only in aurora!
	* replicas are in region
	* serverless

* dynamoDB
	* ssd
	* reads
		* eventually : within 1 sec (async)
		* strongly : after all writes it perform reads (sync)
	* DAX
		* accelerator 
		* cache  that sits between
	* ACID
		* with dynamodb transactions
	* backup
		* ondemand : in the same region
		* PITR : point in time recovery 35 days , incremental , not enable for default , 5 min (latest)
	* read replica multi Region
		* you have to enable streams
			* streams of data make shards for mulltimaster

* documentDB : run mongodb

* keyspace : amazon apache cassandra 
	* cassandra : noSQL db distributed for bigdata solutions 

* QLDB
	* you cant update old data (immutable)
	* cryptocurrency , pharmacy

*  amazon Timestream ,TSDB
	* db for data over time (prometheus)
		* iot , analytics ,

#### Questions and lab
* with RDS be careful about security group (like efs)

# VPC

* subnet cannot span in multiple AZ
* 5 reserved ip
* one only igw
* explicit -> only one route table
* NAT gateway for internet access for private subnet
* NACL 
	* first line of defense 
	* def : allows everything
	* you can block ip
	* outbound
		* ephemeral ports 
			* 1024-65535
			* a random port that server reply on 
		* role number 
			* lower has more value
			* blocks role number lower than 100

* vpc endpoint : traverse private backbone internet of aws
	* interface
		* private ip address(?)
	* gateway
		* endpoint 

* vpc peering: vpc to vpc connection
	* you can only have end to end (no connection via another vpc)

* private link
	* expose your service to thousands of customer vpc
	* only NLB on your vpc and ENI on customer

* cloudhub
	* multiple sites to connect to a vpn

* direct connect
	* physical location
	* directly connect your datacenter to aws 

* **transit gateway** 
	* a hub/router for your cloud 
	* can be cross regional and account 

* aws wavelenght : mobile network

#### question 
* when using peering connections both vpc has to have route table
* there is a limit on vpc peering 
* transitive peering not supported in vpc peering

# Route 53

* top-level domain name -> .com , .ir
* second-level domain ali.me -> ali

* TLD -> NS -> SOA
* TTL low as possible 

* alias is CNAME but for aws resources 
* health check
* simple routing : round robin ?
* weighted 
	* health check id
* failover routing
	* active/passive route

* geolocation
* geoproximity routin 
	* bias
	* must have traffic policies : complex

* latency routing
* multivalue routing 
	* simple routing with healthcheck

# ELB
* types
	* ALB
	* NLB
	* Gateway LB: layer 3 , inline virtual
		* no rules
	* Classic LB : test , dev
		* x-forwarded , sticku session

* Deregistration delay (connection draining)
	* delay for when comming unhealthy
	
* stickiness in target group

# monitoring


#### questions and labs
* flow logs in vpc
* when you create a flow log to write on s3 , the bucket policy change
* flow to CW needs iam
* create alarm based of a filter on a log group
* cloud insight for sql based queries on logs 
* aws athena can be used to run sql commands on logs saved on s3
* CPU util and network throughput is found in CW by default

* 60x time value for cloudwatch statistic 

# HA and scaling

* step scaling
	* avoid thrashing
	* warm-up -> readiness 
	* cool down -> pause autoscale 

* RDS
	* storage cannot be scaled down
	* serverless -> unpredictible 
	* only in multi AZ cluster you can read from read replica

* DynamoDB
	* provisioned 
	* on demand
	* RCU 
		* every unit for 4 kb
	* WRU
		* every unit for 1kb
	
	
# Decoupling
* SQS
	* pull/poll
	* message cant be higher than 256kb 
	* its not encrypted at rest by default
	* visibility timeout
		* message is locks 
	* DLQ
		* dead letter queue
		* alarm
		* for FIFO
	* only FIFO retain order and deduplication
	* only FIFO is supported for SNS

* SNS
	* push
	* message filtering 
	* fanout
		* parrarel sending 

* API gateway
	* REST
	* HTTP
	* Websocket
	* edge-optimize
	* regional
	* private
	* auth
	* cert
	* WAF

* batch: kinda like lambda but uses docker and longer
	* jobs
	* job definition
	* job queues

* Amazon MQ
	* easier migrations
	* rabbitMQ 
	* only private
	* AMQP , MQTT

* Step functions
	* standard
	* express
	* language
	* states
		* pass : passes data 
		* task : single unit of work done
		* choice
		* wait
		* succeed
		* fail
		* parrarel
		* map

* AppFlow
	* thirdparty saas to s3/redshift or ...
	* usecase
		* salesforce to redshift , slack conversations in s3 , zendesk

#### Questions
* SQS standard can process more messages than FIFO
* custom defined policy for sns retries in HTTP endpoint 


# Big data 
 * Redshift
	 * SQL and big
	 * postgres engine 
	 * not for transaction
	 * 2 AZ (no conversion)
	 * incremental snapshot , **you dont have access to the s3**

* Redshift Spectrum
	* query from s3 without loading data to redshift tables

* ETL : extract transform load

* aws EMR : elastic map reduce 
	* help with ETL , web indexing , ML training
	* strorages
		* HDFS 
		* EMRFS
		* local fs
	* nodes
		* primary : master node
		* core : long time workers
		* task : short time workers (spot instance)

* kinesis
	* real time streaming data
	* types
		* data streams -> realtime (fastest)
			* specify shards
		* data firehose -> nearly realtime (more managed by aws)

* kinesis data analytics -> sql

* athena 
	* analyze data in s3 with SQL
	* integrate with quick insight
* aws Glue
![2970f6b3be0d826f768dec097937ea0a.png](../_resources/2970f6b3be0d826f768dec097937ea0a.png)

* quickSight
	* can have users and groups
	* dashboards

* aws Data Pipeline

* MSK
	* apache kafka
	* encrypt at rest by def

* OpenSearch
	* successor to amazon Elasticsearch


# serverless

* lambda
	* 512 mb - 10GB on /tmp
	* compressed size 50 , unzipped 250 
	* evenbridge can trigger it
	* supports till 10GB of RAM

* ECS
	* tasks = container

* fargate
	* serverless of ECS and EKS
	* EC2 VS fargate
		* fargate for shorter tasks
		* fargate pay for use

* eventbridge
	* events
	* rules : send incoming events to right targets 
		* event pattern
		* scheduled
	* eventbus

* EKS-Distro
	* eks managed by you

* ECS anywhere 
	* no ELB
	* SSM , ECS agent , Docker

* Aurora
	* ACU -> aurora capacity unit

* aws X-Ray Daemon 
	* application insights 
	* listen on port 2000
	* collects raw segment data and send to xray api

* aws appSync
	* GraphQL interfaces 
	* combines multiple sources


# Security

* types of attack
	* ddos
	* SYN
		* the sender ignores SYN-ACK and proceeds to sending SYN
	* Amplification
		* Spoofed source ip and send request to a NTP server and the NTP server replies to the victims servers with 3456 Bytes
	* Layer 7 attack

* WAF for layer 7
	* block ip and country

* firewall manager 
	* multiple accounts

* amazon inspector
	* network and ec2 (agent)

* KMS
	* CMK
	* HSM : hardware security module 
		* creates CMK
* cloudHSM
	* dedicated HSM 
	* full controll
	* no automatic key rotation

* parameter store
	* free , no rotation

* share private object in s3
	* presign --expire-in
	* gives a url

* amazon detective
	* root cause

* network firewall
	* physical

#### Questions
* aws shield -> 3-4 layer
* wait 7 days for kms key to be deleted

# Automation

* Cloudformation
	* not all resources
	* Template sections
		* required 
			* version
			* resources 
		* optional
			* Parameter
			* mappings
			* output
			* transform
	* rollback or retain successful ones 
	* by default if stack fails everything else that was created will be deleted

* Beanstalk
	* PaaS

* SystemManager
	* agent
	* playbooks
	* run command
		* refrence parameters like in ansible -> {{ssm:/dev/db_password}}
	* patch manager
	* parameter store
		* hierarchy names -> /dev/squid_conf
	* session manager

# caching
* cloudFront
	* TTL , cant pick edge
	* WAF
	* ssl

* Elasticache
	* sits infront of a RDS
	* memCache
		* caching solution for other DB
		* its not a DB , no failover ,no backup
	* Redis
		* db and caching solution
		* failover + backup

* DAX
	* inside vpc 
	* in memory cache (micro seconds)
	* just for DynamoDB

* GA
	* Anycast IP
	* TCP , UDP
	* accelerator , listener , endpoint
	* ip caching 

# Governance
	
* Organization
	* management , member
	* OU organization unit
	* SCP service control policy

* RAM recource access manager
	* owner cant delete
	* participant cant delete and can provision services in vpc that is shared

* cross-account role access

* aws Config
	* shows configuration history over time
	* per region
	* SNS and eventBridge
	* it doesnt prevent , it just alert
	* automatic remediation

* Cost explorer
	* visualize
	* custom reports
	* can forecast up to 12 months

* Budgets
	* let users know
		* based on
			* cost
			* usage
			* RI usage 
			* Saving plans usage

* CUR cost and usage reports 
	* publish to s3
	* once a day only
	* integrate with athena and ...

* compute optimizer
	* not enabled by default

* Saving plans
	* compute saving -> on demand
	* sagemaker -> everyhting

* trusted advisor
	* best practice
	* based on
		* cost
		* performance
		* security
		* fault tolerent
		* service limits
		* operational excellence

* aws control tower
	* guardRails
		* detective
		* preventive

* aws proton
	* IaC
	* terraform (?!)


# Migration

* snowcone
	* 8tb , 4gb ,  2vcpu
* snowball
	* 48-81 tb
* snowmobile
	* 100PB

* storage gateway -> hybrid
	* file gateway
	* volume gateway
		* isci mount
		* becoming ebs
	* tape gateway
		* glacier

	
* DataSync
	* agent-based
	* NFS smb
	* one time solution

* migration HUB
	* central place

* MGN
	* lift and shift application

# front-end web

* Amplify
	* full stack
	* Hosting
		* framworks and other shit like rendering
	* Studio
		* auth , ready to use components

* Device Farm
	* application testing
	* uses actual tablets and mobiles
	* automated and remote access testing (holy shit!)

* PinPoint
	* engage with customers 
	* project
	* channels
	* segments
	* campaigns
	* journeys
	* message template
	* ML
	* marketing, transactions , campaigns

# Machine Learning

* Comprehend (NLP)
	* detects sentiments
* Kendra
	* intelligent **search** service
* Textract
	* extract text
	* use -> receipts/handwriting/scanned docs to data

* Forecast
	* apply ML to time series data (bitcoin or Iot and shit)

* Transcribe
	* convert audio to text
* Lex
	* chat with automated bot
* Polly
	* convert text to audio (lifelike speech)
* Rekognition
	* face and other things detection 
* sageMaker
	* GroundTruth
	* Notebook : create model
	* Training
	* inference : deploy model
	* online(realtime) and offline
	* Neo
	* decrease cost -> EI elastic inferences

#### Questions
* alexa uses Lex , Polly , Transcribe 

# Media
* Transcoder
	* change format of videos
	* transcode
* Kinesis video streams
	* millions of devices
