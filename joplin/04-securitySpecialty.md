# Threat Detection
* Config
	* regional
	* aggregators -> multi region
	* histories
	* not preventetive

* Trusted advisor
	* cost
	* performance
	* security
	* Fault tolerant
	* quotas

* GuardDuty
	* Detectors
	*  Data Source
	*  Trust ip list
	*  Threat list
	*  Integrated with eventBridge
		*  Events that are caused by GD , are best effort not guaranteed
	*  Stopping GD -> your GD configuration is lost

* EC2 remediate
	* stop
	* delete
	* open a support case
	* market place
* s3 remediate
	* locate the resource
	* find the api call 
	* analyze , maybe they are authorized

* integrate health with eventBridge

* AWS Inspector
	* EC2 , ECR , lambda
	* Network assesment
		* scan EC2 instances , every 24h , no agent
	* Host assesment
		* needs agent
	* publish to security hub
	* export csv , json to s3 , needs encrypt
	* active , suppressed , closed

* ssm
	* patch manager
		* patch baseline (predefined , custom)
			* auto approval
			* scan and install or only scan
			* patch groups
				* the tags must be "Patch Group"
		* aws does not test patches
		* needs s3 access 
	

* AWS Artifact
	* on demand and only on aws services
	* docs are unique to your account
	* dont share 

* AWS trust
	* abusive usage
		* spam
		* port scan
		* DoS

* Amazon Detective
	* ML
	* collects logs from other services
	* needs to be enables + GD enabled as well
	* regional

### Questions
* Organizations can have a chosen **delegated administrator** (can be invited manually also) account for centralizing and aggregating findings — usually a Security Team account.

# Security Logging

* CW
	* log retention from 1 day to ....
	* subscriptions (like kinesis data stream , NOT for S3 )
	* filters
		* up to 2 subscription filters
		* cannot modify them
		* lambda , kinesis 
	* kms for every log group

* CT
	* Management events
		* write and read operations
		* creating and attaching IAM , vpc , disabling CT , ConsoleLogin
	* data events
		* not by default
	* quota = 5 trails
	* first one is free
	* global services can be addressed with us-east-1 in CT
	* digest file in s3 validates logs

* kinesis data firehose
	* 60 seconds , near realtime
	* transform data via lambda when needed
	* subscription filters
* kinesis data streams
	* realtime
	* kinesis agent for sending to kinesis
	* 24h minimum retention
* OpenSearch
	* subscription filter
	* visualize

* VPC flow
	* to CW , S3 , Kinesis fire hose
	* cannot be modified
	* version 2 
	* 


### Questions
* cost effective log solution with no transformation , scalable , integrate with quicksight - > s3 + athena
* event pattern in event bridge is passed down to lambda
* CW subscription filter is not native for s3
* athena supports CSV , JSON , ELB logs , **NOT CLOUD Watch**
* AWS Audit Manager service
	* To provide continuous audits and evidence collection


# Infrastructure Security

* KMS
	* HSM , FIPS 140-2 level 2 validation
	* Custom keys , Fips 140-2 level 3
	* rotations , default is a year
	* scheduled
	* a key has only one policy
	* IAM policy alone is not enough to use kms
	* temp access
	* custom keys
	* aws managed keys
		* cannot manage keys
		* no rotation changes
		* no key policy changes
		* cannot change the 1 year rotation
	* aws owned keys
		* cannot see them , no control
	* data keys **4 kb** 
		* symmetrical
		* outside of aws
		* managed by you
		* encryption use the plaintext and delete it (without kms envolved)
		* decryption uses encrypted data key and send it to kms , get new plaintext to decrypt , delete plaintext
	* EXTERNAL Keys , algorithm
		* wrapping key
		* importToken
		* openssl and wrapping key to create key material and upload with import token
		* key deletion between 7 and 30 days
	* envelope Encryption
		* encrypt plaintext with a datakey and encrypt the datakey with another key
		* a top level plaintext at some level (root key)

* Cloud HSM
	* Auto HA
	* FIPS level 3 , kms doesnt
	*  HSM is single tenant
	*  aws has no access to your HSM
	*  1-28 nodes
	*  use ENI 
	*  not native for aws Services
	*  useCase
		*  TLS
		*  CA
		*  TDE in oracle DB
		*  Java Tools

* WAF
	* rules
		* rule group
	* sets
		* ip 
		* regex
	* web ACL
		* log to anything
	* bot , fraud , captcha use case
	* steps:
		* create a set
		* create web ACL
			* add set in the rule 

* AWS Network Firewall
		* component
			* firewall
			* firewall policy
			* rule group
				* statefull and stateless
					* stateless only can pass , drop , 	forward to stateless rule
			* firewall endpoint should be unique
		* NOT SUPPORT
			* vpc peering
			* virtual private gateway
			* global accelerator
			* amazon provided dns

* AWS Firewall manager
	* centralize
		* waf as well\

* lambda@edge
	* viewer/origin request
* cloudfront functions
	* onlu javascript
* aws shield
	* standard , advance
	* route53 , cloudfront
	* global accelerator
* vpn
	* ipsec for site
	* tls for client

### Question
* valid rule for AWS Network Firewall
	Stateful firewalls monitor and detect states of all traffic and defend base on patterns and flows.

# iam

* NotAction , notResource
* 

### Questions
* identity provider
	* SAML 2.0 federation (e.g., Microsoft AD and Okta) and Web-based federation (e.g., Facebook, Google, and Apple) are valid configurations.

* types of pools within Amazon Cognito?
	* Amazon Cognito has two types of pools: User pools, which are user directories that provide sign-up and sign-in options for your app users, and Identity pools, which provide AWS credentials to grant your users access to other AWS services.

* granting users permissions directly via identity-based policy not user policy

* What is a true statement regarding IAM groups?
	* IAM groups allow us to simplify access management by applying permissions to a single group and not have to apply to separate users

# data protection
* ACM
	* automatic renewal for certs 
	* one way , two way
* ELB
	* classic 
		* fully customized security policies
	* ALB
	* NLB
		* SNI supported
	* GWLB
		* layer 3 , gneve protocol

### Questions
* All ACM certs must live within **us-east-1** in order to operate with Amazon CloudFront.
* You cannot implement unbroken SSL on ALBs
* With **compliance** retention modes, you can never overwrite or delete object versions, or change settings regardless of the user. Not even the **root** user.
* S3 Object Lock supports two retention modes: Compliance and Governance
* ALB do not support TCP 443 listeners and Unbroken TLS/SSL
* Application Load Balancers support Subject Alternative Name (SAN) to map a single TLS to multiple subdomains, AWS WAF integrations for associating web ACLs and rules, and Authentication via OIDC-compatible providers like Amazon Cognito
* ACM validation via email and DNS validation


# management

### recover ebs encrypted with cmk but deleted 
* if ec2 gets restarted on the volume unmounts , the data is lost forever
* add another ebs , create filesystem (mk.xfs) /dev/vdfx , mount /dev/vdfx /x , rsync   

* Direct connect for between regions
* VIF 
	* public
	* private
	* transit
### Questions
* how long do you have to resolve any encryption-related errors before records disappear?
	* The default time is 24 hours before records will disappear.
* fine-grained access policies via roles when using Amazon Athena as a data source for Amazon Quicksight?
	* Athena run-as roles
* 


