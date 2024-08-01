* iam principle
```
"Principal": { "Service": "s3.amazonaws.com" }
or
"Principal": { "AWS": "arn:aws:iam::AWS-account-ID:role/role-name" }
```

* Create iam role aws cli (only trust policy can be configured here)
```
aws iam create-role \
--role-name eksctl-eks-lab-cluster-nodegroup-test2 \
--assume-role-policy-document file://test.json
    
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
```
 # creating policy
 iam:CreatePolicy
 # creating ServiceAccount with eksctl
 iam:GetOpenIDConnectProvider
 cloudformation:*
 iam:GetRole
 iam:DetachRolePolicy
 iam:CreateRole
 iam:TagRole
 iam:DeleteRole
iam:AttachRolePolicy
```