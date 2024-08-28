# foundation
![c55d3247059c0267a1063641eae0f43f.png](../_resources/c55d3247059c0267a1063641eae0f43f.png)

types od services aws provides
![b0d1a2e0a2540761b9f7fec1925f50ed.png](../_resources/b0d1a2e0a2540761b9f7fec1925f50ed.png)

capEx vs opEX -> upfront vs pay as u go

benefits of cloud : HA , elastic , agility , durability

models : iaas paas saas 

public and private and hybrid(direct connect?!	) cloud

region -> AZ -> datacenter

local zone (?1) extentions of aws region

more edge location that regions and AZ because it uses aws backbone network

![956a57a38c62f776333cb758c04ce8f9.png](../_resources/956a57a38c62f776333cb758c04ce8f9.png)
![7cd44278a1878ce0c3049d27017b018c.png](../_resources/7cd44278a1878ce0c3049d27017b018c.png)


# compute technology

* EC2 : elastic : 
on demand , reserved , spot instances , dedicated **Host** , saving plans

reserved and saving plans are 1 - 3 year commit

* LB and Autoscaling and compute optimizer
* LB types
classic: 4/7 , ec2 network 
gateway: 3/4 , network logging and 3rd party
app: 7 , http https
network: 4 , tcp tls , static ip

* Containers -> ECS EKS ECR

* Serverless -> lambda 
fargate : if it takes more than 15 mins u use fargate unless use lambda 
fargate -> message queue 

lambda charges for N request and duration (1 mill a month free)
fargate for cpu and mem u use 

* outpost : hybrid , used for data residency , bring aws to premise 
	* outpost rask 
	* outpost servers 
* lightsail : quickly launch small project ,  small temp env for test deployment (?!)
* batch: run jobs , big work to small batches 
* wavelenght : 5G ultra low latency for mobile network


# storage 

* EBS: HA , scale , snapshot -> nosql DB , ERP CRM
* ssd : better for iops -> read write per second
gp2-3 , io2-3
iops support multi attach 
hdd: better for throughput -> bits per second
st1 
sc1 less throughput

snapshots: incremential , multi az 

* EFS: managed , scale , concurrent use -> web serving
* instance store :  temp , I/O , no bill -> dump , cache 

* S3: bucket , obj has metadata (unique key), 

standard 
intelligent tiering
standart IA : infrequent but fast when needed
one AZ IA
glacier instant
..... flexible : archive , not fast (1,2 retrieve per year)
...... Deep archive
![fc080961b2bb6a1cf334dcef5d7df38b.png](../_resources/fc080961b2bb6a1cf334dcef5d7df38b.png)
ACL and bucket policy 
lifecycle

* xfs : windows
* EDR : disaster recovery

* storage gateway: hybrid storage service , backup + DR (dis recov)+ data proccessing
	* s3 gateway
	* volume gateway : block storage
	* FSx
	* tape : archive 

* aws backup 
	* automated , centralized 
	* integrate with services 

# content delivery 

* cloudFront : 
	* uses edge location to cache
* global accelerator : 
	* uses edge location to find optimal path to region
	* less complexity 
	* built in ddos protection

* VPC 
	* subnet
	* internet gateway
	* route table
	* security group : statefull
	* NACL : stateless

* route 53
	* health check
	* its own routing
	* dns failover 
	* traffic flow feature : simple routing , geolocation routing , latency bases routing 
	* used for private dns in vpc 

* direct connect : for hybrid models  , used for large data transfer 
* aws vpn 
	* site to site 
	* client vpn 

# database technology

* RDS : rows and columns 

* DynamoDB : nosql
* ElastiCache : in memory data cache
* MemoryDB: in memory data store 
	* automatic replicates data 
* Neptune : graph db , relationship
* aurora with mysql compatible

* DMS : database migration service
	* minimal downtime
	* reliable
	* migrate to different db 

* SCT : schema conversion tool , convert db schema/language to aws compatible
	* oracle -> redshift 

# CICD
* codeCommit : git repo
* codeBuild: 	build + test
* codeDeploy
* aws CI/CD pipeline
* cloud9 : IDE

* codeArtifact : nexus

* microservices decoupling	 
	* Queues : SQS 
		* queue system
		* decoupling
		* pull-based 
		* standard , FIFO (only once , no duplicate)
		* short polling(more cost) , long polling
	* Notification : SNS : 
		* sms + email 
		* pub - sub model
		* it has topics that send messages 
	* Events : Event bridge
		* state changes 
		* rules , events , targets 
		* schedule


* SES : simple email service , send richly formatted html

* step functions: 
	* manage logic of a flow (each step is lambda )
	* visualize , loggin , trigger

* IaC : cloudformation : yaml , json , stack

* Elastic beanstalk : you only write code 
	* configures : LB , runtime , webserver , dbs ....
	
* X-ray : diagram with health status , metrics 

# migration and transfer technologies 

* snow family : physical stuff to migrate to aws when you dont have good bandwith ,(data transfer)
	* snowball : 10TB
	* snowball edge : 10TB + processing power before going to aws
	* snowmobile : 10 petaByte , a truck
	* snowcone : to 14 TB , small and portable 

* aws transfer family
	* file sharing and transfer with external parties
		* sftp: ssh ftp
		* as2 : applicability statement 2 , http and https
		* FTPS , FTP 

* datasync : securely transfer data to s3,efs,fsx 
	* for migration , archiving 

* application **discovery** service 
	* you install ASD agent to gather data from your own datacenter and its sent to ADS or for vCenter agent collector(agentless)
	* gather data

* **application migration service** : replicate your vm to aws 
	* replication agent 
	* automated 
	* lift and shift method

* migration hub 
	* central place 
	* integrated 
	* plan and track

# monitoring and logging 

* metric 
	* create charts , alarms 
* logs
* configuration

* cloud watch : watch metrics and such
	* How long are CloudWatch Logs stored by default? Indefinitely
* cloud trail : track the trail , api usage

* managing resources 
	*  tags 
	*  system manager 
		*  take automated actions 
		*  ssm parameter store : pass , strings , license 

* aws health dashboard 
* trusted advisor 
	* advises
		* example: MFA is enabled? is your sg open?public snapshot?

* aws config : does not enforce it audits 
	* AWS Config allows you to set up account-wide rules and detect non-compliant resources.
	* for large number of resources 
	* does not generate audit report

* aws audit manager : audit data  from aws config 
	* prebuilt in auditing **frameworks** 
	* you can define custom frameworks 
	* produces **audit reports** 
	* Find root causes of noncompliance and generate reports.

* well-architected tool
	* for best practices and generate action plans 
	* checks the six pillars of well architecture 

* amazon connect 
	* call center in cloud 
* amazon workspaces
	* provision remote desktops 
* amazon appstream
	* converts applications to SaaS for for employees or end users 

# Security, Compliance, and Governance


* sec of , in the cloud 
* least priviledge 
* iam : who and what
	* automatic rotate credentials over time
* IAM access analyzer 	
* IAM simulator 

* identity center + amazon directory service : federated identity to aws (ex: ur company uses microsoft AD)
* amazon cognito -> auth for users
* STS : temp role for read-only 

* encryption at rest,transit
* key manager service(kms) for RDS EBS
* traffic in vpc is encrypted by def
* ssm parameter store : is like vault
* secrets manager : vault with password rotation

* WAF : protects from common exploits
* network firewall : inspect traffic
* aws shield : for ddos protection

* firewall manager : manages all above 
* guard duty : detects malicious behavior
* inspector : checks for vulnerabilities
* macie: checks s3 buckets 
* ssm : noncompliant resources 
* config : noncompliant resources
* IAM access analyzer: detects externally accessible resources and unused access
* aws health

* security hub : central place for all above , they send info to security hub
	* it determines the best way to take action

* amazon guardduty : collects logs and use ML to detect threats (already threats)

* amazon Detective : helps you investigate security events

* aws Organization : manage multiple accounts 	
	* config
	* service control policies

* aws Control tower : automatic acc creation , best practice configs for 

* aws Artifact : aws docs 

# optimizing cost

* reserved instance
	* standard
	* convertible 	
	* scheduled

* compute optimizer
	* uses cloudwatch to analyze
* storage lens
	* analyze s3 and make recomm

* network in network costs the most , inside AZ cheapest

* pricing calculator
* aws budgets : receive SNS alert 
* cost explorer: gain insight on actual aws usage (visualize)
* cost and usage reports : most detailed , store on s3 

* billing conductor: create billing groups within aws Organization
* tags works for bills as well

* aws IQ : freelancers
* aws managed services : pre-X 
* professional services : team of aws experts 
* aws activate : support for startups