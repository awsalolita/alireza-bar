* Region then CIDR or ip range then subnets 
* while creating subnets : which vpc , what AZ , whats the ip range (subset of VPC ip ranges)
* public and private 
* igw , vgw (internet and virtual)
* vgw : for adding connection to on premise via customer gateway 
* you can add route tables to every layer (subnets , gateways and so on)
* there are 5 reserved ip addresses in every subnet (router , broadcast , network , dns , future use cases )

Peering connections : connect 2 vpc 

Traffic Mirroring: security and monitoring appliances for deep packet inspection

Transit gateways : central hub  to route traffic between your VPCs, VPN connections, and AWS Direct Connect connections (?) 


# route tables

main and custom 
main is applied to the vpc 
the default configuration of the main route table is to allow traffic between all subnets in the local network

if you use custom route table , the subnet wont use the main table anymore
 custom tables have local route by default
 

# security 

ACL is stateless  -> in and out -> subnet level -> everything is allowed 
`
you allow inbound 443 and outbound range 1025-65535. That’s because HTTP uses port 443 to initiate a connection and will respond to an ephemeral port.`

security group -> statefull -> no in and out just one -> instance level -> incoming is blocked , by default there is a rule that allows all outbound traffic

**TIED TO A VPC**
`security groups are stateful, meaning they will remember if a connection is originally initiated by the EC2 instance or from the outside and temporarily allow traffic to respond without having to modify the inbound rules.   

If you want your EC2 instance to accept traffic from the internet, you’ll need to open up inbound ports`

* inbound and outbound:
`
When users first create a security group, it has no inbound rules. Therefore, no inbound traffic is allowed until users add inbound rules to the security group. However, security groups have a default outbound rule that allows all outbound traffic from the resource. Users can remove or add outbound rules to allow only specific outbound traffic.`