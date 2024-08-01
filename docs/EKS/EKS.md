https://www.eksworkshop.com/docs

# 0.0 Create Iam
# 0 Create Cluster
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

# 1 Creating NodeGroups 
* use
* IAM role for the NodeGroups Must have `Workerrole` , `CNIrole`  , `AmazonEC2ContainerRegistryReadOnly` and the Trustpolicy for ec2
```
aws eks create-nodegroup \
    --cluster-name eks-lab-cluster \
    --nodegroup-name worknodes-1 \
    --subnets "subnet-043290da2540411ed" "subnet-0a61f664f94c79380" "subnet-01bd67b025355e892" --node-role arn:aws:iam::678879639233:role/eksctl-eks-lab-cluster-nodegroup-test2
```


# 2 Kubeconfig and Rollout coredns
* create api and fargate profile as soon as possible
* access the cluster with cloudshell 
```
aws eks update-kubeconfig --region region-code --name k8s
kubectl rollout restart -n kube-system deployment coredns
```

# 3 IRSA or Pod Identity
## IRSA
### Creating OIDC
* check if you have one
```
cluster_name=mycluster
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
```
```
cluster_name=mycluster
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve
```
* with console provider url from eks console and audience `sts.amazonaws.com`
### OPTION A : Create with eksctl
```
eksctl create iamserviceaccount \
    --name iampolicy-sa \
    --namespace default \
    --cluster mycluster \
    --role-name "eksRole4serviceaccount" \
    --attach-policy-arn <PolicyARN> \
    --approve \
    --override-existing-serviceaccounts
```
### OPTION B : Create roles and SA seprately

* Create role with web identity trustpolicy  or with [this custom trustpolicy](../../common_policies/EfsEKS_truspolicy.json)
* create [sa like this](../../eks/ServiceAccount.yaml)

## Pod Identity
### create eks-pod-identity-agent add on
* a role with `pods.eks.amazonaws.com` trust policy and `sts:AssumeRole`, `sts:TagSession`
* creating it via console
* cli
```
cluster_name=mycluster
ROLE=<arn>
aws eks create-pod-identity-association --cluster-name $cluster_name \
  --role-arn $ROLE \
  --namespace default --service-account mysa
```

# 4 install ingress controller 
## setup ingress 
* tag the subnets 
* for internet facing , tag subnet
```
kubernetes.io/role/elb: 1 
kubernetes.io/cluster/${your-cluster-name}: owned
```
* for interval
```
kubernetes.io/role/internal-elb: 1
kubernetes.io/cluster/${your-cluster-name}: owned
```
* if the subnets are also used by non-EKS resources 
```
kubernetes.io/cluster/${your-cluster-name}: shared
```
## installation
* ing controller
* create policy , role and sa 
[official doc](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.8/deploy/installation/)

```
curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.8.1/docs/install/iam_policy.json
```

* [permissions needed](../IAM.md)
```
aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam-policy.json

```
```
cluster_name="mycluster"
accid=11111
eksctl create iamserviceaccount \
  --cluster=$cluster_name \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::$accid:policy/AWSLoadBalancerControllerIAMPolicy \
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
  --set clusterName=mycluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller 
  --set vpcId=vpc-xxxxxxxx \
  --set region=region-code \
```


# 5 helm chart

```
helm repo add app https://aahemm.github.io/helm-microservice
helm upgrade --install app --values values.yaml app/app --version 0.10.0
```

# storage
* default storage class cant be used on fargate
* on ec2 its probably ok
## EFS (EC2) (only IRSA)

* this is iam role for csi driver , policy: `AmazonEFSCSIDriverPolicy` 
* create a role with the following
### OPTION A eksctl 
```bash
export cluster_name=mycluster
export role_name=AmazonEKS_EFS_CSI_DriverRole
eksctl create iamserviceaccount \
    --name efs-csi-controller-sa \
    --namespace kube-system \
    --cluster $cluster_name \
    --role-name $role_name \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy \
    --approve
```
```bash
TRUST_POLICY=$(aws iam get-role --role-name $role_name --query 'Role.AssumeRolePolicyDocument' | \
    sed -e 's/efs-csi-controller-sa/efs-csi-*/' -e 's/StringEquals/StringLike/')
aws iam update-assume-role-policy --role-name $role_name --policy-document "$TRUST_POLICY"
```
### OPTION B Create role and SA seprately
* add aws add-on for efs to deploy the pods for it
* dont create CSI driver (for ec2) and create storage class [file](../eks/efs-fargate/)
### Restric anonymous
EC2    
* for the `role` used for the csi driver give access
* pv and sc with iam mountoption
EFS
* for the `Fargatepodrole` give access
* pv and sc with iam mountoption

## Fargate EFS
* only Create the objects in k8s
* create csi driver and storageClass [file](../eks/efs-fargate/)

## EBS CSI driver

* create iam role
```bash
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
```bash
eksctl create addon --name aws-ebs-csi-driver --cluster k8s --service-account-role-arn arn:aws:iam::<>:role/AmazonEKS_EBS_CSI_DriverRole --force

kubectl patch storageclass gp2 -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
```
* go create [storageclass](../eks/ebs/sc-pv-pvc.yaml)


# Secrets
## AppConfig
* in the [secretmanager doc](../SecretManager.md)
## Secret Manager and ParameterStore ASCP (file and mount)
* Create SA with ONLY IRSA for the application
* mount a file in the name of the secret
* `DescribeSecret` and `GetValue` only needed
* `ssm:GetParameters` for parameter store
```
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm install secret secrets-store-csi-driver/secrets-store-csi-driver --set enableSecretRotation=true --set syncSecret.enabled=true

kubectl apply -f https://raw.githubusercontent.com/aws/secrets-store-csi-driver-provider-aws/main/deployment/aws-provider-installer.yaml
```
* Create `SecretProviderClass` [here](./eks/Secret/SecretProviderClass_ALL.yaml)
* objectType for parameter store `ssmparameter`
* [Patch you deployment](./eks/Deployment/ADD_SecretCSI.yaml) or create Deployment [like this](./eks/Deployment/deploy_SecretCSI.yaml)
```
kubectl patch deployment app --patch "$(cat patch.yaml)"

```

## Secret Manager ESO (Secret)
* iam for the eso IRSA for the helm chart
`GetSecretValue` `DescribeSecret` only needed
```
"secretsmanager:GetResourcePolicy",
"secretsmanager:GetSecretValue",
"secretsmanager:DescribeSecret",
"secretsmanager:ListSecretVersionIds"
```
* values.yaml
```
serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: "<ARNrole>"
  name: "eso-service-account"
``` 
```
helm repo add external-secrets https://charts.external-secrets.io
helm install eso external-secrets/external-secrets  --values ./values.yaml
```
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: store
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: eso-service-account
```
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: esecret
spec:
  refreshInterval: 1m
  secretStoreRef:
    name: store
    kind: SecretStore
  target:
    name: mysecret
    creationPolicy: Owner
  data:
    - secretKey: <K8sSecretKey>
      remoteRef:
        key: <secretmanagerName>
        property: name # you can use event.backend.username like json 
    - secretKey: dbPassword
      remoteRef:
        key: <secretmanagerName>
        property:   # or backend.password
```
```
fuck=booohooo
```
# access to others to see k8s objects in console (Config-Map)
* [above this](https://docs.aws.amazon.com/eks/latest/userguide/auth-configmap.html#aws-auth-configmap)
## system:masters (cluster-admin)
* Create clusterrole , Clusterrolebinding(Group)
```bash
eksctl create iamidentitymapping --arn arn:aws:iam::590183933432:user/arpjoker --group system:masters --cluster mycluster
```
## Access only via api

* Create ClusterRole , ClusterRoleBinding
```
aws eks create-access-entry --cluster-name mycluster --principal-arn arn:aws:iam::590183933432:role/myrole --type STANDARD  --kubernetes-groups arpjoker
```
## get what iam have access to what
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
# Cluster Scaling
## karpenter
* tag the `cluster` and `subnets` and `security group` `karpenter.sh/discovery: ${CLUSTER_NAME}`
* create [iam's](./eks/Karpenter/0_iam.md)
* change the `arn` and the `clustername`
```bash
helm upgrade --install karpenter oci://public.ecr.aws/karpenter/karpenter  \
--version 0.37.0 \
--set "settings.clusterName=mycluster" \
--set "serviceAccount.annotations.eks\.amazonaws\.com/role-arn=<ARN>" \
--set controller.resources.requests.cpu=1 \
--set controller.resources.requests.memory=1Gi \
--set controller.resources.limits.cpu=1 \
--set controller.resources.limits.memory=1Gi \
--set replicas=1 \
--wait
```
* apply `NodePool` and `NodeClass` [here](./eks/Karpenter/0_NodePool.yaml)
* change nodeaffiniy of `karpenter`  
```
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: karpenter.sh/nodepool
                operator: DoesNotExist
              - key: eks.amazonaws.com/nodegroup
                operator: In
                values:
                  - <nodegroup_name>
```
* you can add for `core-dns` `metric server` too 
## CAS (cluster auto scaler)



# AutoScale Pods
## HPA
* metric server
* apply hpa to deployments
## KEDA
* installation
* iam to hap access to cloudwatch
```bash
helm repo add kedacore https://kedacore.github.io/charts
helm upgrade --install keda kedacore/keda \
  --version "v2.14.2" \
  --namespace keda \
  --create-namespace \
  --set "podIdentity.aws.irsa.enabled=true" \
  --set "podIdentity.aws.irsa.roleArn=${KEDA_ROLE_ARN}" \
  --wait # access to cloudwatch
```


# CloudWatch addon

* it needs the `CloudWatchAgentServerPolicy` and attach it to the **worker node** ot make **IRSA** 
* SA `cloudwatch-agent` and `amazon-cloudwatch`

```bash
aws iam attach-role-policy \
--role-name my-worker-node-role \
--policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy 
```
```bash
eksctl create iamserviceaccount \
  --name cloudwatch-agent \
  --namespace amazon-cloudwatch --cluster my-cluster-name \
  --role-name my-service-account-role \
  --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
  --role-only \
  --approve
```

# Metric server

```

```