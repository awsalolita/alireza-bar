# for login and push permissions
* includes eks describe
```json
                "ecr:CompleteLayerUpload",
                "eks:DescribeCluster",
                "ecr:UploadLayerPart",
                "ecr:InitiateLayerUpload",
                "ecr:BatchCheckLayerAvailability",
                "ecr:PutImage",
                "ecr:GetAuthorizationToken"
```
# Permissions Policies
* exclude
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "new statement",
      "Effect": "Deny",
      "Principal": "*",
      "Action": ["ecr:PutImage"],
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalArn": [
            "arn:aws:iam::AWS-ACOUNT-ID:role/service-role/pyei-challenge-codebuild-service-role"
          ]
        }
      }
    }
  ]
}
```