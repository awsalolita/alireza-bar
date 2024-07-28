# configs for the launch template
1. Enable `detailed monitoring` 
2. Check the Secuirty group of the ec2
3. attach ssm iam profile
4. attach efs
5. write user-data
6. cpu Credit -> unlimited

# ELB 
1. check the subnet
2. check the security group
3. health check additional for `404` code if needed 

# ASG
* first create without scaling policy
* Enable the asg group monitoring

## simple scaling 
* set the wait time to 180
## Health check and Cooldown
* must be the same values

# cloudwatch
* `WarmPoolWarmedCapacity` and `GroupInServiceCapacity` for number of instances in asg metrics
* in `Per AppELB, per TG Metrics` choose `RequestCountPerTarget` , what scales the app (change the metric to sum per second or minute)
    * this too `TargetResponseTime` 
* do math
* for cpuutil `EC2 > By Auto Scaling Group`
