# VPC
* common security group while creating ec2
* attach EIP to ENI
* you can have multiple nat gateways
* vpc peering with the same ip
	* route tables with specifi /32 ip route for the specific instance
* **reachablity analyzer**
* vpc flow logs can be used in ENI , subnet lvl , vpc lvl
* vpc peering can handle public dns over the peering connection for private ip address
## Questions
NACL
* for accessing the internet via natgateway , if you set the nacl to allow only private addresses , it cannot connect to the internet
AWS Shield
* AWS Shield Standard mitigates attacks that occur at Layers 3 and 4 of the OSI model.
* AWS Shield is a managed Distributed Denial of Service (DDoS) protection service
```
AWS WAF is a web application firewall that helps protect your web applications or APIs against common web exploits.
Amazon Inspector is an automated security assessment service that helps improve the security and compliance of applications deployed on AWS.
Amazon Macie is a security service that uses machine learning to automatically discover, classify, and protect sensitive data in AWS.
Amazon GuardDuty is a threat detection service that continuously monitors for malicious activity and unauthorized behavior to protect your AWS accounts and workloads.
AWS Security Hub gives you a comprehensive view of your high-priority security alerts and compliance status across AWS accounts.
```
IPV6
* NAT GATEWAY cant be used , only igw
* All AWS-owned IPv6 IP pools are assigned to your VPC with a **/56 CIDR.**
* bound by the number of ipv4
FireWall Manager
* It enforces deployment of Web Application Firewall ACLs.
* It enforces deployment of AWS Shield Advanced protection policies.
* It can report findings to AWS Security Hub.
* DOESNT supports the configuration of VPC security groups and Network ACLs.

AWS Service Catalog allows organizations to create and manage catalogs of IT services that are approved for use on AWS. Deploying applications via AWS Service Catalog can help ensure that deployments meet organizational compliance needs, but it cannot compare recorded configuration changes against desired configurations.

AWS packet level details of vpcs
* VPC Traffic Mirroring
* 

# Route 53
* having a subdomain as a new hosted zone
	* create the record in the root hosted zone

* using route53 as private dns in the vpc
	* add the vpc to the hosted zone
	* enable dns in vpc
	* change DHCP options sets

* **Resolver** , +2 Address
	* resolves dns queries from aws resources within vpc
	* different from vpc router 
	* vpc CIDR +2 (the ip , like -> 10.0.0.2)
	* vpc ROUTER is in every subnet (Range +1 , like 10.0.3.1)

* GateWay LB 
	* analyze the network in between (send them for analetics)
	* layer 3-4
* algorithms
	* RoundRobin
	* Least outstanding request
	* Hash (only NLB)
* ELB cross-zone loadbalancing and Access Logging
*  tcp health checks doesnt have path
*  attributes for algorithms and stickiness in target group

* stickiness
	* ALB
		* can be from application and can be from elb
		* cookie
			* `AWSALB` `AWSELB`

* GLB
	* doesnt have a FQDN
	* routed via the route table 

* 5 target groups to a single service


* field level encryption
	* encrypted at edge
	* seperate http and https tunnels
	* tls between edge location and servers

* private viewer access ???
*  geographical restrictions
	*  CF built in
* Origin Shield region
* lambda in vpc
	* Hyperplane ENI , one per private subnet
	* usecases
		* lambda + rds

* EKS
	* creates ENI in the subnets of workers
	* Control plane is managed by aws

* API Gateway
	* http
	* restful
	* certs for api gateway needs to be in the same region

* ec2 enhanced networking
	* single root i/o virtualization
		* lower cpu utilization , because it bypasses the hypervisor
		* ENA faster than VF 

* EFA
	* elastic fabric adapter
	* for high performance computing and machine learning

* placement groups 
	* cluster
		* single AZ , low latency ,
	* partition
		* logical segments
		* no shared resources , their own rack
	* spread
		* different hardware
		* multiple az

## Questions
* privateLink is aws endpoint services
	* publish your own private api
	* its like vpc endpoints but for custom things i guess
* NACL
	* inbound : 80 , 443 , 22 , ephemeral 
* AWS Global Accelerator is a service in which you create accelerators that are assigned Anycast IPs closer to your customers to improve the performance of your applications.
* CloudFront reaches out to the origin. When the **first byte** of content arrives at the edge location, it is then forwarded on to the end user. 
* First, create an ALIAS record for awesome-guru.com and point it to the ALB as a target. Next, create a CNAME record for www.awesome-guru.com and point it to awesome-guru.com.
	* you cant create 2 alias to the same thing

# Hybrid
* gateways
	* IGW
	* VGW
		* attached to only one vpc
		* use cases
			*  site to site vpn
				*  static and dynamic route learning
			*  Direct Connect
				*  only dynamic rout learning
		*  you need to set ASN (autonomous system number)
	* TGW

* routes learned by the VGW need to be added to the route table manually or with
	* route propagation 
	* enabled in route table


* in route table
	* **the most specific route is preferred but local ones have priority**
	* static routes over propagated routes (when matching)
	* DIrect connect > Static vpn > BGP vpn

* BGP
	* port 179
	* eBGP and iBGP
* prefixes prefrence
	* highest weight 
		* weight for another BPG is 0
	* highest local prefence 
	* shortest AS path
	* lowest metric
* path = i -> internal
* path = NUM -> AS number
* eBGP over iBPG
* weight only applies to the local routers
* metric attribute , lower the better


* aws VPN
	* IPSec

* customer gateway device
## Question
* AWS VPN CloudHub is a simple hub-and-spoke model that you can use with or without a VPC. Use this approach if you have multiple branch offices and existing internet connections and would like to implement a convenient, potentially low-cost hub-and-spoke model for primary or backup connectivity between these remote offices
* AWS Accelerated Site-to-Site VPN uses AWS Global Accelerator (GA) to route traffic from on-premises to an AWS edge location that is closest to your customer gateway device. It must use TGW VPN attachments and is an optional feature that must be enabled.


# Transitive Network
* Transit VPC
	* software based vpns
	* attach vpc to its

* TGW to another region
	* transit gateway peering
		* in attachment , you can create peering connection
		* you need to create static routes for the peering routes (in both regions)