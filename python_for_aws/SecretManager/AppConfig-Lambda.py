import json
import urllib3

http = urllib3.PoolManager()


def lambda_handler(event, context):
    # TODO implement

    application_name = 'myapplication'
    environment_name = 'myenv'
    config_profile_name = 'myconfig'

    re = http.request('GET',f"http://localhost:2772/applications/{application_name}/environments/{environment_name}/configurations/{config_profile_name}")
    
    
    print(json.loads(re.data))
    
    return {
        'statusCode': 200
    }
