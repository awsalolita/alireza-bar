#create
eksctl utils associate-iam-oidc-provider --region <region> --cluster <your-cluster-name> --approve



curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.0/docs/install/iam_policy.json

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicyALB \
    --policy-document file://iam-policy.json

eksctl create iamserviceaccount \
  --cluster=<cluster-name> \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicyALB \
  --override-existing-serviceaccounts \
  --region <region-code> \
  --approve

helm repo add eks https://aws.github.io/eks-charts

helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
    --namespace kube-system \
    --set clusterName=<your-cluster-name> \
    --set serviceAccount.create=false \
    --set serviceAccount.name=aws-load-balancer-controller

kubectl get deployment -n kube-system aws-load-balancer-controller -w

## same AZ of the subnet you deployed the EKS cluster
# Public Subnets should be resource tagged with: kubernetes.io/role/elb: 1 

# Private Subnets should be tagged with: kubernetes.io/role/internal-elb: 1

# Both private and public subnets should be tagged with: kubernetes.io/cluster/${your-cluster-name}: owned

# or if the subnets are also used by non-EKS resources kubernetes.io/cluster/${your-cluster-name}: shared

