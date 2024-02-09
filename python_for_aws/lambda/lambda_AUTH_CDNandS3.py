import base64

def lambda_handler(event, context):
    # Your deployment's basic auth credentials
    username = 'ali'
    password = 'ali'
    correct_auth_value = 'Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()

    # Extracting the request from the CloudFront event
    request = event['Records'][0]['cf']['request']
    headers = request.get('headers', {})

    # Checking for basic auth header
    auth_value = headers.get('authorization', [{'value': ''}])[0]['value']
    if auth_value == correct_auth_value:
        # If the authentication is correct, return the request to CloudFront for continued processing
        return request

    # If authentication is incorrect, return a 401 Unauthorized response
    response = {
        'status': '401',
        'statusDescription': 'Unauthorized',
        'body': 'Unauthorized',
        'headers': {
            'www-authenticate': [{'key': 'WWW-Authenticate', 'value': 'Basic'}]
        },
    }
    return response
