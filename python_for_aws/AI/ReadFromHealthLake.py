import boto3
import json
import base64
import time
import datetime
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
from botocore.endpoint import URLLib3Session
import os 
import string

REGION = os.environ['REGION']
DATASTORE_ID = os.environ['DATASTORE_ID']

def lambda_handler(event, context):

    minified_entries = query_lake()
    print(minified_entries)
    data = flatten_data(minified_entries)
    
    result = {
        "data" : data
    }

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(result)
    }

def flatten_data(minified_entries):
    minified_entities = []
    
    for entry in minified_entries: 
        for entity in entry['entities']:
        
            minified_entity = {
                "resource_id" : entry['resource_id'],
                "entity_id" : entity['Id'],
                "text": entity['Text'],
                "category": entity['Category'],
                "type": entity['Type'],
                "traits": entity['Traits'],
            }
        
            minified_entities.append(minified_entity)
            
            try:
                for attribute in entity['attributes']:
                    minified_attribute = {
                        "resource_id" : entry['resource_id'],
                        "entity_id" :  attribute['id'],
                        "text": '[' + entity['text'] + '] ' + attribute['text'],
                        "category": attribute['category'],
                        "type": attribute['type'],
                        "traits": '-',
                    } 
                    
                    minified_entities.append(minified_attribute)
            except KeyError:
                pass
    
    
    return minified_entities
    
    
def query_lake():
    # Replace region and healthlake_url with your solutions method for specifying these values
    
    docs = {
        "id":""
    }
    
    service = 'healthlake'
    region = REGION
    datastoreid = DATASTORE_ID
    healthlake_url = f"https://{service}.{region}.amazonaws.com/datastore/{datastoreid}/r4/"
    
    headershl = {
        'Host': f"{service}.{region}.amazonaws.com", 'Content-Type': 'application/json'
    }

    # Perform a GET to HealthLake
    hldocrefendpoint = healthlake_url + 'DocumentReference'
    
    request = AWSRequest(method='GET', url=hldocrefendpoint, headers=headershl)
    SigV4Auth(boto3.Session().get_credentials(), service, region).add_auth(request)    
    session = URLLib3Session()
            
    request_result = session.send(request.prepare())
    encoded_result = request_result.text
    result = json.loads(encoded_result)

    minified_entries = []
    entries = result['entry']
    for entry in entries:
        
        minified_entry = {
            "resource_id" : entry['resource']['id'],
            "entities" : []
        }
        
        contents = entry['resource']['content']
        print(len(contents))
        for content in contents:
            encoded_data = content["attachment"]["data"]
            data = base64.b64decode(encoded_data).decode('utf-8').replace("'",'"')
            extensions=json.loads(data)
            sub_extensions = extensions['extension']
            for sub_extension in sub_extensions:
                if(sub_extension['url'] == 'http://healthlake.amazonaws.com/aws-cm/detect-entities/'):
                    sub_sub_extensions = sub_extension['extension']
                    for sub_sub_extension in sub_sub_extensions:
                        if(sub_sub_extension['url'] == 'http://healthlake.amazonaws.com/aws-cm/detect-entities/raw-response'):
                            
                            entities_json = sub_sub_extension['valueString']
                            for entity in entities_json:
                                del entity['BeginOffset']
                                del entity['EndOffset']
                                del entity['Score']
                                
                                try:
                                    traits = entity['Traits']
                                    trait_text = ""
                                    for trait in traits:
                                        del trait['Score']
                                        if trait_text != "":
                                            trait_text = trait_text + ", "
                                        trait_text = trait_text + trait['Name']
                                        entity["Temp_Traits"] = trait_text
                                except KeyError:
                                    pass
                         
                                try:
                                    attributes = entity['Attributes']
                                    for attribute in attributes:
                                        del attribute['Score']
                                        del attribute['RelationshipScore']
                                        del attribute['RelationshipType']
                                        del attribute['BeginOffset']
                                        del attribute['EndOffset']
                                        del attribute['Traits']

                                except KeyError:
                                    pass
                        
                                try:
                                    entity['Traits'] = entity['Temp_Traits'] 
                                    del entity['Temp_Traits']
                                except:
                                    pass
                                
                                
                                json_formatted_str = json.dumps(entity, indent=2)
                                
                                minified_entry['entities'].append(entity)
        
        minified_entries.append(minified_entry)
    return minified_entries