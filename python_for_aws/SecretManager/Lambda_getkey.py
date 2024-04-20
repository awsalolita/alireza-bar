# first add layer for secret manager
# iam permissions
# 

#### secret manager
import os
import urllib3
import json

http = urllib3.PoolManager()
headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
url = "http://localhost:" + \
    '2773' + \
    "/secretsmanager/get?secretId=" + \
    '<secret name>'

r = http.request( 'GET' , url, headers=headers)
secret = json.loads(r.data)["SecretString"] # load the Secrets Manager response into a Python dictionary, access the secret
final = json.loads(secret)
#### parameter store



import os
import urllib3
import json

http = urllib3.PoolManager()
headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
url = "http://localhost:" + \
    '2773' + \
    "/systemsmanager/parameters/get/?name=" + \
    '<parameter>' + '&withDecryption=true'
response = http.request("GET", url, headers=headers)
response = response.data.decode()
response = json.loads(response)['Parameter']['Value']