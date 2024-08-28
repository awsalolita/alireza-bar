
# Helm chart

* Values file [here](../../eks/values.yaml)

```bash
helm repo add app https://aahemm.github.io/helm-microservice
helm upgrade --install app --values values.yaml app/app --version 0.10.0
```
* after installing patch the deployment and change the `limit` and `request`
```
kubectl patch deployment app --patch "$(cat patch.yaml)"

kubectl edit deploy app
```

# HPA

* install
``` bash
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm upgrade --install metrics-server metrics-server/metrics-server --set containerPort=10251 --set-string "defaultArgs[0]=--cert-dir=/tmp" --set-string "defaultArgs[1]=--kubelet-preferred-address-types=InternalIP\,ExternalIP\,Hostname" --set-string "defaultArgs[2]=--kubelet-use-node-status-port" --set-string "defaultArgs[3]=--metric-resolution=10s" --set-string "defaultArgs[4]=--kubelet-insecure-tls" --version 3.11.0
```
* get the resources being used by the pods
```
kubectl top pods
```
