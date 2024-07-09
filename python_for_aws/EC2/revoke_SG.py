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



### GET SECURITY GROUPS BY TAGS
client = boto3.client('ec2')
security_group_tag = {'Name': 'cloudfront_g', 'AutoUpdate': 'true', 'Protocol': 'http'}

filters = list()
for key, value in security_group_tag.items():
    filters.extend(
        [
            {'Name': "tag:" + key, 'Values': [value]}
        ]
    )
response = client.describe_security_groups(Filters=filters)

### Add a rule to a security group

def add_permissions(client, group, permission, to_add):
    if len(to_add) > 0:
        add_params = {
            'ToPort': permission['ToPort'],
            'FromPort': permission['FromPort'],
            'IpRanges': to_add,
            'IpProtocol': permission['IpProtocol']
        }

        client.authorize_security_group_ingress(GroupId=group['GroupId'], IpPermissions=[add_params])

    return len(to_add)

### Revoke a rule from a security group
def revoke_permissions(client, group, permission, to_revoke):
    if len(to_revoke) > 0:
        revoke_params = {
            'ToPort': permission['ToPort'],
            'FromPort': permission['FromPort'],
            'IpRanges': to_revoke,
            'IpProtocol': permission['IpProtocol']
        }

        client.revoke_security_group_ingress(GroupId=group['GroupId'], IpPermissions=[revoke_params])

    return len(to_revoke)