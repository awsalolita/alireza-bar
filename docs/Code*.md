# Structure

* `buildspec.yaml`: CodeBuild uses the commands and parameters in the buildspec file to build a Docker image
* `appspec.yaml`: CodeDeploy uses the appspec file to select a task definition
* `taskdef.json`: for ECS Task def

# Aws cli
* Create repo
```bash
aws codecommit create-repository \
    --repository-name pipeline-source-code \
    --repository-description "Repository for AWS News application source code" \
    | jq -r '.[].cloneUrlSsh'
```
* clone
```bash
git clone codecommit://MyDemoRepo
```








# buildspec example
```yaml
version: 0.2
phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws --version
      - ACCOUNT_ID=$(echo $CODEBUILD_BUILD_ARN | cut -f5 -d ':') && echo "The Account ID is $ACCOUNT_ID"
      - echo "The AWS Region is $AWS_DEFAULT_REGION"
      - REPOSITORY_URI=$ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$ACCOUNT_ID-application
      - echo "The Repository URI is $REPOSITORY_URI"
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $REPOSITORY_URI
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=$COMMIT_HASH
  build:
    on-failure: ABORT
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $REPOSITORY_URI:$IMAGE_TAG .
      - docker tag $REPOSITORY_URI:$IMAGE_TAG $REPOSITORY_URI:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image...
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - echo Writing image definitions file...
      - printf '[{"name":”myimage","imageUri":"%s"}]' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json
      - printf '{"ImageURI":"%s"}' $REPOSITORY_URI:$IMAGE_TAG > imageDetail.json
artifacts:
    files: 
      - imagedefinitions.json
      - imageDetail.json
      - appspec.yaml
      - taskdef.json
```

# appspec example
``` yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: <TASK_DEFINITION>
        LoadBalancerInfo:
          ContainerName: "application"
          ContainerPort: 80

```

# taskdef example
```bash
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
AWS_REGION=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r .region) 
FAMILY=$(aws ecs list-task-definition-families --status ACTIVE --output text | awk '{print $NF}') 
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text) 
printf "You are using $AWS_REGION region\nYour task definition family is $FAMILY\nYour account ID is $ACCOUNT_ID\n"
cat << EOF > ~/environment/taskdef.json
{
    "containerDefinitions": [
        {
            "name": "application",
            "image": "<IMAGE_NAME>",
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 80,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "cicd-logs",
                    "awslogs-region": "$AWS_REGION",
                    "awslogs-stream-prefix": "ecs"
                },
            },
        }
    ],
    "family": "$FAMILY",
    "taskRoleArn": "arn:aws:iam::$ACCOUNT_ID:role/ecsTaskExecutionRole",
    "executionRoleArn": "arn:aws:iam::$ACCOUNT_ID:role/ecsTaskExecutionRole",
    "networkMode": "awsvpc",
    "status": "ACTIVE",
    "compatibilities": [
        "EC2",
        "FARGATE"
    ],
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "256",
    "memory": "512",
    "tags": [
        {
            "key": "Name",
            "value": "GreenTaskDefinition"
        }
    ]
}
EOF

```