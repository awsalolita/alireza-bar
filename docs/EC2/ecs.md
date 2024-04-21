

1. edit task with json , add this to ecs task definition (under volumesFrom) , add task role
```
            "linuxParameters": {
                "initProcessEnabled": true
            },
```
2. needs a **task role**
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel"
            ],
            "Resource": "*"
        }
    ]
}
```
with this trust policy
```
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

3. update ecs service to have 

```
aws ecs update-service --service  myservice --cluster myCluster   --enable-execute-command   --force-new-deployment
aws ecs execute-command --cluster <clusterName> --task "<ARN>" --container <container> --interactive --command "/bin/sh"
```
* https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/
* https://alexanderhose.com/how-to-execute-commands-to-manage-your-containers-in-aws-ecs/##setup-of-iam-roles-%F0%9F%91%A5

4. IMP , when you enable service connect , you can find your service with -> "Discovery.DNS:port"
5. YOU cannot create ELB for the service after creation