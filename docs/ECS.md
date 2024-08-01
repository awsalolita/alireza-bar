# Cluster
* Do not contain aws , ecs in the name
* update security group
# TaskDef
* Container's cpu and memory should add up to the overall cpu and memory
# after cloudformation
* Create and then edit `roles` 
* `logging` for fargate -> in taskexecutionrolw
* edit iam for ecs task execution to access secret manager
# Service
4. IMP , when you enable service connect , you can find your service with -> "Discovery.DNS:port"
5. YOU cannot create ELB for the service after creation



# ECS EXEC
1. edit task with json , add this to ecs task definition (under volumesFrom) , add task role
```
            "linuxParameters": {
                "initProcessEnabled": true
            },
```
2. needs a **task role**
* attach one of these
```
arn:aws:iam::aws:policy/AmazonSSMFullAccess
arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
arn:aws:iam::aws:policy/AmazonSSMManagedEC2InstanceDefaultPolicy
arn:aws:iam::aws:policy/AWSCloud9SSMInstanceProfile
```
* or create a policy
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

# ENV

* get from Secret Manager in env in serice config
* print them to a file like
ENTRYPOINT
```
/bin/sh,-c
```
CMD
```
"name=$(echo $myenv | cut -d '\"' -f 4) && id=$(echo $myenv | cut -d '\"' -f 8) && echo -e \"name=$name\nid=$id\" > ali.txt && nginx -g \"daemon off;\""
```

OR
```
{
  "name": "John",
  "age": 30,
  "city": "New York"
}
```
```
grep -o '"name": *"[^"]*' data.json | sed 's/"name": *"//' > tmp_name && \
grep -o '"age": *[0-9]*' data.json | sed 's/"age": *//' > tmp_age && \
grep -o '"city": *"[^"]*' data.json | sed 's/"city": *"//' > tmp_city && \
echo "Name: $(cat tmp_name)\nAge: $(cat tmp_age)\nCity: $(cat tmp_city)" > output.txt
```

# health check
```
CMD-SHELL, curl -f http://localhost/ || exit 1
```

# EBS
* Create A role with ecs `trustpolicy` and `*Infra*` roles 
* T2 instances CANNOT Attach ebs