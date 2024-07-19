
# Helm chart

* Values file [here](../../eks/values.yaml)

```
helm repo add app https://aahemm.github.io/helm-microservice
helm install microservice app/app --values values.yml --version 0.10.0
```
