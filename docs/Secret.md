# Secretman Script
* my image `docker.io/arpjoker/awssecret`
```
touch test
docker run -e AWS_ACCESS_KEY_ID=AKIAQ3EGS4QEHXIY6S2X -e AWS_SECRET_ACCESS_KEY=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  -e AWS_REGION=us-east-1  -v ./test:/app/test arpjoker/awssecret python3 main.py  appconfig myapp:myenv:myconfig json test
```