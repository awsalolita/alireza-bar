import boto3

def lambda_handler(event, context):
    # Extract the security group ID from the AWS Config event
    security_group_id = event['detail']['resourceId']
    ec2 = boto3.client('ec2')

    # Remove the inbound rules that allow 0.0.0.0/0
    try:
        ec2.revoke_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': '-1', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            ]
        )
        print(f"Removed open inbound rules for {security_group_id}")
    except Exception as e:
        print(e)
