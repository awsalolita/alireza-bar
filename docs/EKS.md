
# start
* create api and fargate profile as soon as possible

* access the cluster with cloudshell 
```
aws eks update-kubeconfig --region region-code --name my-cluster
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