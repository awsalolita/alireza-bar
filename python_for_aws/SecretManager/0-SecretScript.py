import sys
import boto3
import json
import os
import yaml
import configparser
from configparser import ConfigParser

def get_parameter_from_ssm(parameter_name, region):
    client = boto3.client('ssm',  region)
    response = client.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']

def get_secret_from_secrets_manager(secret_name , region):
    client = boto3.client('secretsmanager', region)
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

def get_config_from_appconfig(application, environment, config_profile, region):
    client = boto3.client('appconfigdata', region)
    # Start the configuration session
    response = client.start_configuration_session(
        ApplicationIdentifier=application,
        EnvironmentIdentifier=environment,
        ConfigurationProfileIdentifier=config_profile
    )
    session_token = response['InitialConfigurationToken']
    
    # Get the latest configuration
    config_response = client.get_latest_configuration(
        ConfigurationToken=session_token
    )
    
    return config_response['Configuration'].read().decode('utf-8')

def save_to_config_file(key, value, format, filename):
    try:
        value_dict = json.loads(value)
    except json.JSONDecodeError:
        print("Failed to decode JSON")
        sys.exit(1)
    
    if format == 'json':
        try:
            with open(filename, 'r') as configfile:
                existing_data = json.load(configfile)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}
        existing_data.update(value_dict)
        with open(filename, 'w') as configfile:
            json.dump(existing_data, configfile, indent=4)
    elif format == 'yaml':
        try:
            with open(filename, 'r') as configfile:
                existing_data = yaml.safe_load(configfile) or {}
        except FileNotFoundError:
            existing_data = {}
        existing_data.update(value_dict)
        with open(filename, 'w') as configfile:
            yaml.dump(existing_data, configfile, default_flow_style=False)
    elif format == 'equal':
        config = ConfigParser()
        try:
            config.read(filename)
        except FileNotFoundError:
            pass
        config['DEFAULT'] = {**config['DEFAULT'], **value_dict}
        with open(filename, 'a') as configfile:
            for key in value_dict:
                configfile.write(f'{key}="{value_dict[key]}"\n')
    else:
        print("Unknown format. Use 'json', 'yaml', or 'equal'.")
        sys.exit(1)

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 main.py <ssm|secret|appconfig> <parameter_name> <format> <filename>")
        sys.exit(1)

    service = sys.argv[1]
    parameter_name = sys.argv[2]
    format = sys.argv[3]
    filename = sys.argv[4]
    region = os.getenv('AWS_REGION', 'us-east-1')
    if service == 'ssm':
        value = get_parameter_from_ssm(parameter_name , region)
    elif service == 'secret':
        value = get_secret_from_secrets_manager(parameter_name , region)
    elif service == 'appconfig':
        application, environment, config_profile = parameter_name.split(':')
        value = get_config_from_appconfig(application, environment, config_profile , region)
    else:
        print("Unknown service. Use 'ssm', 'secret', or 'appconfig'.")
        sys.exit(1)

    save_to_config_file(parameter_name, value, format, filename)
    print(f"Appended {parameter_name} to {filename} in {format} format")

if __name__ == '__main__':
    main()
