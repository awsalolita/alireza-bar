
# Create Cluster
```
eksctl create cluster \
--name mycluster \
--nodegroup-name worknodes-1 \
--node-type t3.medium \
--nodes 2 \
--nodes-min 1 \
--nodes-max 4 \
--managed \
--version 1.29 \
--region ${AWS_DEFAULT_REGION}
```

# Creating NodeGroups 
* IAM role for the NodeGroups Must have `Workerrole` , `CNIrole`  , `readonlyECR` and the Trustpolicy for ec2
```
aws eks create-nodegroup \
    --cluster-name eks-lab-cluster \
    --nodegroup-name worknodes-1 \
    --subnets "subnet-043290da2540411ed" "subnet-0a61f664f94c79380" "subnet-01bd67b025355e892" --node-role arn:aws:iam::678879639233:role/eksctl-eks-lab-cluster-nodegroup-test2
```

# start
* create api and fargate profile as soon as possible

* access the cluster with cloudshell 
```
aws eks update-kubeconfig --region region-code --name k8s
kubectl rollout restart -n kube-system deployment coredns
```


# IAM OIDC provider
* create one to use iam with your cluster
* check if you have one
```
cluster_name=k8s
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4

```

* setup (install eksctl before)
```
cluster_name=k8s
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve

```






# storage
* default storage class cant be used on fargate
* on ec2 its probably ok

## efs
* iam role for csi driver 
* create a role (not for fargate)
```
export cluster_name=my-cluster
export role_name=AmazonEKS_EFS_CSI_DriverRole
eksctl create iamserviceaccount \
    --name efs-csi-controller-sa \
    --namespace kube-system \
    --cluster $cluster_name \
    --role-name $role_name \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy \
    --approve
TRUST_POLICY=$(aws iam get-role --role-name $role_name --query 'Role.AssumeRolePolicyDocument' | \
    sed -e 's/efs-csi-controller-sa/efs-csi-*/' -e 's/StringEquals/StringLike/')
aws iam update-assume-role-policy --role-name $role_name --policy-document "$TRUST_POLICY"

```
* add aws add-on for efs (not for fargate!?) to deploy the pods for it



# install ingress controller 
* ing controller
* create policy , role and sa 
```
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy.json
```
```
aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json

```
```
eksctl create iamserviceaccount \
  --cluster=<> \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::<>:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve
```

* add helm repo
```
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks
```
```
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=k8s \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set vpcId=vpc-xxxxxxxx \
  --set region=region-code \
```
# setup ingress 
* tag the subnets 
* for internet facing , tag subnet
```
kubernetes.io/role/elb -> 1 
```
* for interval
```
kubernetes.io/role/internal-elb -> 1
```

# ingress fargate and ec2
```
https://stackoverflow.com/questions/71432239/target-group-binding-not-getting-created-for-an-alb
```


# secret from secret manager
* using csi driver will create file which is not be usable most of the times
* lets attach iam

* create a policy and role for a service account
```
eksctl create iamserviceaccount --name my-service-account --namespace default --cluster <k8s> --role-name my-role --attach-policy-arn arn:aws:iam::<111122223333>:policy/my-policy --approve
``` 
* use the sa in your deployment

# helm chart

```
helm repo add app https://aahemm.github.io/helm-microservice
helm repo update
helm install app app/app --values ./values.yaml
```
# IAM to Deployment
```
eksctl create iamserviceaccount \
    --name iampolicy-sa \
    --namespace containers-lab \
    --cluster eks-lab-cluster \
    --role-name "eksRole4serviceaccount" \
    --attach-policy-arn arn:aws:iam::$ACCOUNT_NUMBER:policy/eks-lab-read-policy \
    --approve \
    --override-existing-serviceaccounts
```
```
kubectl set serviceaccount \
 deployment eks-lab-deploy \
 iampolicy-sa -n containers-lab
```

# EBS CSI driver

* create iam role
```
eksctl create iamserviceaccount \
    --name ebs-csi-controller-sa \
    --namespace kube-system \
    --cluster k8s \
    --role-name AmazonEKS_EBS_CSI_DriverRole \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
    --approve

```

* create add on
```
eksctl create addon --name aws-ebs-csi-driver --cluster k8s --service-account-role-arn arn:aws:iam::<>:role/AmazonEKS_EBS_CSI_DriverRole --force

kubectl patch storageclass gp2 -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
```
* go create storageclass




# karpenter
# access to others to see k8s objects in console (Config-Map)

## system:masters (cluster-admin)
* Create clusterrole , Clusterrolebinding(Group)
```
eksctl create iamidentitymapping --arn arn:aws:iam::590183933432:user/arpjoker --group system:masters --cluster jam-cluster
```
# Access only via api

* Create ClusterRole , ClusterRoleBinding
```
aws eks create-access-entry --cluster-name jam-cluster --principal-arn arn:aws:iam::590183933432:role/myrole --type STANDARD  --kubernetes-groups arpjoker
```
# get what iam have access to what
```
eksctl get iamidentitymapping --cluster my-cluster --region=region-code
```

# delete cni role after creating SA

```
 eksctl create iamserviceaccount \
    --name aws-node \
    --namespace kube-system \
    --cluster eks-lab-cluster \
    --role-name AmazonEKSVPCCNIRole \
    --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
    --override-existing-serviceaccounts \
    --approve
```
```
kubectl delete Pods -n kube-system -l k8s-app=aws-node
```
```
aws iam detach-role-policy --role-name AmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
```