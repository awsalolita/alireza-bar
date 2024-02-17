import boto3

elbv2 = boto3.client('elbv2')
elbv2.deregister_targets(
    TargetGroupArn='arn:aws:elasticloadbalancing:region:account-id:targetgroup/my-targets/1234567890123456',
    Targets=[
        {
            'Id': 'instance-id',
        },
    ]
)

# sg modify 
ec2 = boto3.client('ec2')
# Assuming 'sg-forensicsonly' is the security group allowing only inbound from the forensic instance
ec2.modify_instance_attribute(InstanceId='instance-id', Groups=['sg-forensicsonly'])
