# Api Key
* api key
```
curl -H "x-api-key: AQiTWLjMXvS4MRboF4Kp7N7VxrGjOYgi"
```

# nlb for private
* private
* need vpc endpoint
* api key
* vpc link needs NLB
* in nlb untick the inforce privatelink sg

# Path
* override the path

# URL
```
https://<api-id>.execute-api.region.amazonaws.com/<stage>/<Lambda>
```
# CLI
```bash
aws apigateway get-resources --rest-api-id <>
aws apigateway get-stages --rest-api-id <>
aws apigateway  test-invoke-method --rest-api-id puspzvwgb6 --resource-id puspzvwgb6 --http-method GET
aws apigateway get-method  --rest-api-id s33ppypa75 --resource-id prod --http-method GET 
aws apigateway test-invoke-method --rest-api-id {copied-api-id} --resource-id {copied-resource-id} --http-method GET --path-with-query-string '/items/56438794' --region us-east-1
```


# Security
restrict
* resource policy example
* can enable iam as well
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:*:*:*",
      "Condition": {
        "IpAddress": {
          "aws:VpcSourceIp": "10.199.0.0/24"
        }
      }
    },
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:*:*:*",
      "Condition": {
        "StringNotEquals": {
          "aws:sourceVpc": "vpc-03fb377a4f7684f0c"
        }
      }
    }
  ]
}
```

* request API without sigv4
```python
def call_api(api_id: str, api_key=None): 
    host = api_id+'.execute-api.'+region+'.amazonaws.com'
    base_url = f'https://{host}/api'
    get_url = f'{base_url}/{os.environ["api_resource"]}'

    response = requests.get(get_url, headers={'x-api-key': api_key}, timeout=2)
    return response
```
* request API with sigv4 (iam auth)
```python
# Simplifies making Amazon SigV4 calls with the python requests library
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

def call_api(api_id: str, api_key=None): 
    host = api_id+'.execute-api.'+region+'.amazonaws.com'
    base_url = f'https://{host}/api'
    get_url = f'{base_url}/{os.environ["api_resource"]}'

    # Get authentication token - SigV4 (no header)
    auth = BotoAWSRequestsAuth(aws_host=host, aws_region=region, aws_service='execute-api')
    # response = requests.get(get_url, headers={'x-api-key': api_key}, timeout=2, auth=auth)
    response = requests.get(get_url, timeout=2, auth=auth)
    return response
```


# QueryStringParameter
* add them in the method request
* in Integration Request add mapping template `application/json`
```json
{
  "name" : "$input.params('<querystring>')"
}
```

# Lambda
* when you enabled lambda proxy integration
	* you get pathparameters and such
* but when you dont you only get the body that you send

## Rest Api event
* to get the path and such
```python
event['httpMethod'] == 'GET'
event['resource'] == '/items'
event['httpMethod'] == 'GET' and event['resource'] == "/items/{id}"
# to get {id} for example
ids = event['pathParameters']['id']
``` 
### HTTP Api event
* get path
```python
path = event['rawPath']
arg = path.split('/')
```
# CORS
* Enable access from another hostname 