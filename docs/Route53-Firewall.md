# Network Firewall
### route tables
* igw (this fucking route should send the ip cidr of the fucking natgateway to the firewall endpoint)
* firewall
* public subnet (where the nat gateway is)
* private subnet
* default behaviour is pass all

* Create rule group
* `HOME_NET` is the source ip

* Create firewall policy

* Create a firewall in a subnet
* route the traffic to the firewall with route tabel `gateway loadbalancer` `vpce-XXXX`

### suricata rule group 
* drop non tls traffic
```
drop tcp any any <> any 443 (msg:"SURICATA Port 443 but not TLS"; flow:to_server,established; app-layer-protocol:!tls; sid:2271003; rev:1;)
```
# route 53
* enable query logging
### domain list 
* create the list
* create rule group
* associate with a vpc

