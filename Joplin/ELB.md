# Types
1. APPLICATION LB, HTTP/HTTPS ,  LAYER 7
2. NETWORK LB , TCP/UDP/TLS , LAYER 4 
3. GATEWAY LB , IP ,  LAYER 3+4  

# Components 
* Listener 
* Target group and their healthchecks(/monitoring)
* Rules (balance based on these rules)

# ALB
* route based on URL path
* send response directly to client (redirects and such)
* TLS offloading (using ACM)
* auth (can connect to LDAP and ...)
* security group
* round robin and outstanding request (where req vary in complexity) algorithms for routing
* sticky sessions with **cookies**

* the app sees the ip of **ELB**

# NLB

routes based on 
* protocol 
* source ip and port
* destination ip and port 
* tcp sequence number

**sticky sessions via source ip**
* tls offloading 
* can handle millions of requests (i think because layer 4)
* it can have ip address 
* the app sees the ip of **clients**