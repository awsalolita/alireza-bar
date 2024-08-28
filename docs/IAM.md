# Principle
* iam principle
```json
"Principal": { "Service": "s3.amazonaws.com" }
or
"Principal": { "AWS": "arn:aws:iam::AWS-account-ID:role/role-name" }
```


# AWS CLI
* Create iam role aws cli (only trust policy can be configured here)
```bash
aws iam create-role \
--role-name eksctl-eks-lab-cluster-nodegroup-test2 \
--assume-role-policy-document file://test.json
    
```
* who am i (user)
```bash
aws sts get-caller-identity
aws iam get-user
aws iam list-attached-user-policies --user-name <Username>
aws iam list-user-policies --user-name <>
aws iam list-policy-versions --policy-arn <>
aws iam get-policy-version --policy-arn <> --version-id <>

```
* who am i (role)
```bash
aws sts get-caller-identity
aws iam list-attached-role-policies --role-name <role>
aws iam get-policy-version --policy-arn <> --version-id <v1>
```
* get lambda iam policy
```bash
aws lambda get-policy --function-name Level6
```

* Attach Policy to the created role
```
aws iam attach-role-policy \
--policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
--role-name eksctl-eks-lab-cluster-nodegroup-test2
```

* Update Assume Policy (Trust Policy)
```
aws iam update-assume-role-policy  \
    --role-name eksctl-eks-lab-cluster-nodegroup-test \
    --policy-document file://test.json
```

# iam policy that grants creating iam policies
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "iam:CreateInstanceProfile",
                "iam:RemoveRoleFromInstanceProfile",
                "iam:AddRoleToInstanceProfile",
                "iam:PassRole",
                "iam:DeleteInstanceProfile"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```
# iam policy for creating eks resources
### creating policy
iam:CreatePolicy
### creating ServiceAccount with eksctl
iam:GetOpenIDConnectProvider
cloudformation:*
iam:GetRole
iam:DetachRolePolicy
iam:CreateRole
iam:TagRole
iam:DeleteRole
iam:AttachRolePolicy

# Tag Based permissions
* `aws:TagKey` -> checks the tag keys
* `aws:RequestTag/Project` -> API Actions 
* `aws:ResourceTag/Project` -> the tag that the resource have
example [here](../common_policies/IAM-TagRoleEqualEC2.json)

