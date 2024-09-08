# Task 2: Traffic from VPC2 cannot reach anywhere
### Clue 1:Packet Walk Through
Use Systems Manager and connect to the Instance in VPC2. Very similar to Task 1, think about each hop the packet takes and check the configuration:

Starting with VPC2, check the route table for 10.1.0.0/24 subnet (PrivateVPC2RT-PrivateVPC2). There should be a default route of 0.0.0.0/0 pointing to the TGW.

Since there is only a single route table used by the Transit Gateway, you'll notice that the packet will take an identical path we saw in Task 1; the Transit Gateway route table uses 0.0.0.0/0 via the Egress VPC attachment. The packet is then routed by another default route of 0.0.0.0/0 by 192.168.2.0/24 subnet route table (PrivateNATRT-EgressVPC) in the Egress VPC. The next hop is the Nat Gateway.

Where does the packet go next? What's the next hop? Does it look OK?

### Clue 2:Check Route Tables
In the first clue we traced the packet all the way to the NAT Gateway. If you check the route table that is used by the NAT Gateway (PublicNATRT-EgressVPC) you'll also notice a default route 0.0.0.0/0 pointing to the Internet Gateway (igw).

So far everything looks correct, however, if you check the return traffic in the PublicNATRT-EgressVPC route table you'll notice a route of 10.0.0.0/16.

This route only covers VPC1 subnet. This route is excluding the 10.1.0.0/24 subnet which affects the return traffic from the Internet or Egress VPC hosts.

Here is a step by step walk through to fix the issue:

1- In the Console, go to VPC and click on Route Tables.

2- Select the public subnet route table (PublicNATRT-EgressVPC). You will find that the following entry exists:

10.0.0.0/16 tgw-(tgw-id)

To fix this issue, replace this route with:

10.0.0.0/8 tgw-(tgw-id)

This will cover subnets in VPC1 and VPC2 and future subnets that maybe added in the future in the 10.x.x.x range.

To validate this task, connect to the EC2 instance from Systems Manager as follows:

1- From the AWS Console, search for Systems Manager

2- From Systems Manager, click Session Manager

3- Click the Start Session Button

4- Select PrivateVPC2Subnet-Instance

5- Issue the command curl amazon.com from PrivateVPC2Subnet-Instance

You should get an output similar to the following:

sh-4.2$ curl amazon.com

301 Moved Permanently

sh-4.2$

The response code you're looking for is 301. Providing 301 in the Answer section completes this task.

# Task 3: Traffic Segmentation for the Two Spoke VPCs
### Clue 1:Consider Separate Route Domains
The Transit Gateway by default has a single route table (Route Domain). In order to have more granular control over traffic flow, you can create separate route tables and associate those route tables with different VPCs.

The route tables become separate entities and you can have completely different routes in each table. Your goal is make sure that VPC1 cannot have a route pointing to VPC2 and vice versa.

### Clue 2:Segmenting VPC1 and VPC2 Traffic
The following step by step walk through will meet the Security team requirement:

    Note: Make sure you are working with Transit Gateway Route Tables under the Transit Gateways section NOT VPC Route Tables.
1- Go to VPC > Transit Gateway Route Tables.

2- Select route table TGWRouteTable-us-east-1

3- Click the Association tab and delete all attachments associated with the route table

Note: You can only associate an attachment with a single route table. Deleting an Association from a route table breaks routing for that attachment.
4- Create two new route tables. Use the following names for Name Tags and select the Transit Gateway in the Transit Gateway ID window.

     Egress_access 
     Spoke_access
5- In the Egress_access route table, click the Association tab and select VPC1. Repeat for VPC2.

Click the Routes tab in the Egress_access route table. Create the following routes:

 Static route for 192.168.0.0/16 via the Egress-Attachment.
 Static route for 10.0.0.0/8 and select "Blackhole".
Note: This will cause the TGW to drop any traffic coming in from either VPC1 or VPC2 destinated to 10.0.0.0/8.

6- In the Spoke-access route table click the Association tab and select the Egress-Attachment.

Click the Routes tab and create the following static routes:

 A route for each of the Spokes (subnet 10.0.0.0/16 and 10.1.0.0/16) via their respective attachments.
 A route for all other traffic including internet traffic. This route will have 0.0.0.0/0 via the Egress-Attachment
To validate this task, connect to the EC2 instance from Systems Manager as follows:

1- From the AWS Console, search for Systems Manager

2- From Systems Manager, click Session Manager

3- Click the Start Session Button

4- Select PrivateVPC1Subnet-Instance

5- Issue the command ping 10.1.0.100 from PrivateVPC1Subnet-Instance. Paste the complete first response line in the Answer section:

From 10.1.0.100 icmp_seq=1 Destination Host Unreachable

If the ping times out simply type timeout


# Task 4: The Instance in VPC2 cannot talk to the instance in the Egress private subnet.
### Clue 1:Packet Walk Through
Use Systems Manager and connect to the Instance in VPC2. Think about the path the packet takes to reach the EgressVPCPrivateSubnet-Instance:

Starting with VPC2 route table, you should see a default route 0.0.0.0/0 pointing to the TGW. Originally we were using a single route table in the Transit Gateway so if you did Task 3 correctly, then you would be using the route table used by the Spokes. If you followed Task 3 Clue#2 that would be the Egress-access route table. The Egress-access route table is used by the Spoke VPCs to access the Egress VPC and the Internet.

The Egress-access route table will have a route of 192.168.0.0/16 with the Egress-Attachment as next hop. The Subnet ID for this Egress-Attachment is subnet 192.168.2.0/24 which uses PrivateNATSubnet-EgressVPC route table.

Examine the PrivateNATSubnet-EgressVPC route table. Does it look OK?

### Clue 2:Check Route Tables
In Clue#1 you examined the PrivateNATSubnet-EgressVPC route table. If you haven't spotted the issue, here is a step by step walk through:

1- In the Console, go to VPC > Route Tables

2- Select PrivateNATRT-EgressVPC route table

3- Examine route 10.0.0.0/16 – TGW (tgw-id)

Notice this route only covers subnet for VPC1. Change the route to:

10.0.0.0/8 – TGW (tgw-id)

Now you can ping 192.168.2.100 from instance in VPC2.

To validate this task, connect to the EC2 instance from Systems Manager as follows:

1- From the AWS Console, search for Systems Manager

2- From Systems Manager, click Session Manager

3- Click the Start Session Button

4- Select PrivateVPC2Subnet-Instance

5- Issue the command ping 192.168.2.100 from PrivateVPC2Subnet-Instance in VPC2.

6- Paste part of the response

all the way up to and including the ":" in the Answer section as mentioned below:
while pasting the output, please exclude "time="
64 bytes from 192.168.2.100:

Pasting in the above output in the Answer section completes this task.
