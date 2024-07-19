import json
import urllib3
import boto3




def lambda_handler(event, context):
    # TODO implement

    application_name = 'myapplication'
    environment_name = 'myenv'
    config_profile_name = 'myconfig'

    appconfigdata = boto3.client('appconfigdata')
    
    scs = appconfigdata.start_configuration_session(
    ApplicationIdentifier=application_name,
    EnvironmentIdentifier=environment_name,
    ConfigurationProfileIdentifier=config_profile_name)
    initial_token = scs['InitialConfigurationToken']
    glc = appconfigdata.get_latest_configuration(ConfigurationToken=initial_token)
    config = glc['Configuration'].read()
    
    config = json.loads(config)
    
    print(config)
    

    
    return {
        'statusCode': 200
    }
