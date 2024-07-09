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