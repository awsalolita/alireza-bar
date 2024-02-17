
### CLOUDWATCH EVENT RULE  FOR EC2 INCIDENT RESPONSE ###

import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    instance_id = event['instance_id']
    
    # Step 1: Identify attached volumes
    try:
        attached_volumes = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['BlockDeviceMappings']
        #security_groups = response['Reservations'][0]['Instances'][0]['SecurityGroups']
        print(f"Found volumes: {attached_volumes}")
    except Exception as e:
        print(f"Error describing instance: {e}")
        return {"error": str(e)}
    
    # Step 2: Take snapshots of the volumes
    for volume in attached_volumes:
        volume_id = volume['Ebs']['VolumeId']
        try:
            snapshot = ec2.create_snapshot(VolumeId=volume_id, Description=f"Forensic snapshot of {volume_id} from {instance_id}")
            print(f"Snapshot created: {snapshot['SnapshotId']}")
        except Exception as e:
            print(f"Error creating snapshot for volume {volume_id}: {e}")
    
    # Step 3: Quarantine the instance - assuming quarantine security group ID is 'sg-xxxx'
    quarantine_sg_id = 'sg-xxxx'
    try:
        ec2.modify_instance_attribute(InstanceId=instance_id, Groups=[quarantine_sg_id])
        print(f"Instance {instance_id} moved to quarantine security group {quarantine_sg_id}")
    except Exception as e:
        print(f"Error quarantining instance: {e}")
        return {"error": str(e)}
    
    return {"message": "Incident response completed successfully"}
