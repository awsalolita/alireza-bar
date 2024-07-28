# Configure Cloudwatch agent
## iam role
* `CloudWatchAgentServerPolicy`
## ssm
* first ssm `AWS-ConfigureAWSPackage` with package named `AmazonCloudWatchAgent`
* then `AmazonCloudWatch-ManageAgent`
## commandline
* install rsyslog
```
sudo yum install -y rsyslog
sudo systemctl enable rsyslog --now
```
* install agent
```
sudo yum install amazon-cloudwatch-agent
```
* cwagent permissions for a file
```
sudo setfacl -m u:cwagent:rx /var/log/secure
```

* create configfile and run the service
```
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
## after creating config.json
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
```

* status of the service
```
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status
```


# Creating metric filter from logfiles

### for making alarms
* `authentication failure` pattern in the filter for the metric

* Create a filter , test it on the log group

* then you will Create a metric namespace , metric name 

* Metric value `1` , Default Value `0` when counting

# CloudWatch log insights

* default
```
fields @timestamp, @message
| sort @timestamp desc
| limit 20 
```
* Parsing
```
fields @timestamp, @message
| parse @message "* * * * * * *" as id , number ,eni , db , sourceip , port , other
| FILTER port=3306 and db='10.0.4.160'
| display  id , number , eni , db , sourceip ,port
| stat count() by sourceip

```
ALTERNATIVE (vpcflowlog)
```
fields @srcAddr
| stats count(*) as callsOnPort3306 by srcAddr
|filter dstPort = 3306
| sort by callsOnPort3306 desc
| limit 20
```

* Success http calls number
```
fields @message
| filter @message like /200/
| stats count() by bin(2h)
```


* Network interface regex
```
fields @timestamp, @message
| filter @message like /3306/
| parse @message /(?<NetworkInterface>\seni-.*?\s)/
| display @timestamp, NetworkInterface
```

* vpcflow log not legitimate
```
fields @srcaddr, @dstport
|parse '* * * * * * * * * * * * * *'  as version, account_id, interface_id, srcaddr, dstaddr, srcport, dstport, protocol, packets, bytes, start, end, action, log_status
| stats count(*) as callsNotOnPort3306 by srcaddr, dstport
|filter dstport != 3306 and dstport != 80
| sort by callsNotOnPort3306 desc
| limit 20

```
* vpcflow log ssh and rdp port
```
fields @srcaddr, @dstport
|parse '* * * * * * * * * * * * * *'  as version, account_id, interface_id, srcaddr, dstaddr, srcport, dstport, protocol, packets, bytes, start, end, action, log_status
| filter dstPort in [22 , 3389]
| limit 20
```

* CloudTrail , last iam user 
```
fields @timestamp , @message , sourceIPAddress
|filter userIdentity.type = "IAMUser"
| filter eventName="ConsoleLogin"
| display eventName , sourceIPAddress ,  userIdentity.userName
| sort @timestamp desc
```

* SSHGroup
```
parse '* * * * * * * * * * * *' as Mon, day, timestamp, destip, id, msg1, msg2, msg3, srcIp, msg5, destPort, msg7
| filter msg1 = 'Connection'
| sort by @timestamp desc

```
or
```
parse '* * * * * * * * * * * *' as Mon, day, timestamp, destip, id, msg1, msg2, msg3, msg4, srcIp, msg6, destPort
| filter msg2 = 'user'
| sort by @timestamp desc

```

# EventBridge
* cron expression  
`rate(1 minute)`   
`cron(*/1 * * * ? *)`


# xray
* sdk in your code and then install xray agent
* `recorder` `middleware` 
# enable xray on lambda
```
aws lambda update-function-configuration \
    --function-name genre_function \
    --tracing-config Mode=Active
```
```
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()
```

# Contributer insights
Example for the querylog of route53    
* Create a rule