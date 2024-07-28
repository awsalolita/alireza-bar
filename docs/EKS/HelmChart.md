
# Helm chart

* Values file [here](../../eks/values.yaml)

```
helm repo add app https://aahemm.github.io/helm-microservice
helm install microservice app/app --values values.yml --version 0.10.0
helm upgrade --install test --values values.yml app/app
```
# HPA

* install
``` 
helm upgrade --install metrics-server metrics-server/metrics-server --set containerPort=10251 --set-string "defaultArgs[0]=--cert-dir=/tmp" --set-string "defaultArgs[1]=--kubelet-preferred-address-types=InternalIP\,ExternalIP\,Hostname" --set-string "defaultArgs[2]=--kubelet-use-node-status-port" --set-string "defaultArgs[3]=--metric-resolution=15s" --set-string "defaultArgs[4]=--kubelet-insecure-tls" --version 3.11.0
```
* get the resources being used by the pods
```
kubectl top pods
```
