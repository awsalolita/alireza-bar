import boto3
import json
import base64
import time
import datetime
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
from botocore.endpoint import URLLib3Session
import os 
REGION = os.environ['REGION']
DATASTORE_ID = os.environ['DATASTORE_ID']

comprehend_medical = boto3.client('comprehendmedical')

def lambda_handler(event, context):

    quantity = 0
    text=""
    record = event['Records'][0] 
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    s3Path = "s3://" + s3bucket + "/" + s3object
    local_file_name = '/tmp/current_job.json'
    s3 = boto3.client('s3')
    s3.download_file(s3bucket, s3object, local_file_name)
    
    f = open (local_file_name, "r")
    data = json.loads(f.read())
    for transcript in data['results']['transcripts']:
        text = transcript['transcript']
    f.close()
    
    send_to_lake(text)

def create_extension(docText):
   # Format Comprehend Medical result into HealthLake DocumentReference's extension format
   try:
        response = comprehend_medical.detect_entities_v2(
           Text=docText
        )
        entities_value = {}
        entities_value["url"] = "http://healthlake.amazonaws.com/aws-cm/detect-entities/raw-response"
        entities_value["valueString"] = response["Entities"]
        sub_sub_extension = {}
        sub_sub_extension["extension"] = [entities_value]
        sub_sub_extension["url"] = "http://healthlake.amazonaws.com/aws-cm/detect-entities/"
        extension = {}
        extension["extension"] = [sub_sub_extension]
    
        return extension
   except Exception as e:
      print(e)

def createDocRef(docText, transcriptionTime, subject, idEncounter, 
                    encounterStartTime, encounterEndTime, serviceProvider, 
                    serviceProviderDisplay, practID, practDisplay):

    encodedText = base64. \
        b64encode(str(docText).encode('ascii') ). \
        decode('utf-8')
    jsonDocRefTemplate = {
            "resourceType":"DocumentReference",
            "date": transcriptionTime,
            "custodian":{
               "reference": serviceProvider,
               "display": serviceProviderDisplay
            },
            "subject":{
               "reference":"subject"
            },
            "author":[
               {
                  "reference":"practID",
                  "display":"practDisplay"
               }
            ],
            "context":{
               "period":{
                  "start": encounterStartTime,
                  "end": encounterEndTime
               },
               "encounter":[
                  {
                     "reference":"idEncounter"
                  }
               ]
            },
            "type":{
               "coding":[
                  {
                     "system":"http://loinc.org",
                     "code":"75519-9",
                     "display":"Encounter"
                  }
               ]
            },
            "category":[
               {
                  "coding":[
                     {
                        "system":"http://hl7.org/fhir/us/core/CodeSystem/us-core-documentreference-category",
                        "code":"clinical-note",
                        "display":"Clinical Note"
                     }
                  ]
               }
            ],
            "content":[
               {
                  "attachment":{
                     "data": encodedText,
                     "contentType":"text/plain"
                  }
               }
            ],
            "status":"superseded"
        }
    return( jsonDocRefTemplate )
    

def send_to_lake(text):
    service = 'healthlake'
    region = REGION
    datastoreid = DATASTORE_ID
    healthlake_url = f"https://{service}.{region}.amazonaws.com/datastore/{datastoreid}/r4/"
    headershl = {
        'Host': f"{service}.{region}.amazonaws.com", 'Content-Type': 'application/json'
    }
    # define a datetime
    current_time = datetime.datetime.now()
    #define a timedelta representing the employee notice
    interval = datetime.timedelta(minutes = 15)
    final_time = current_time+interval
    docText = text
    transcriptionTime = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    subject = 'subject'
    idEncounter = '1'
    encounterStartTime = transcriptionTime
    encounterEndTime = final_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    serviceProvider = 'serviceProvider'
    serviceProviderDisplay = 'serviceProviderDisplay'
    practID = 100
    practDisplay = 'practDisplay'
    comprehend_medical_result = create_extension(docText)
    # Create the DocumentReference with encounter specific parameters
    jsonDocRef = createDocRef(comprehend_medical_result, transcriptionTime, subject, idEncounter, 
                    encounterStartTime, encounterEndTime, serviceProvider, 
                    serviceProviderDisplay, practID, practDisplay)
    # POST to HealthLake
    hldocrefendpoint = healthlake_url + 'DocumentReference'

    ipayload = json.dumps(jsonDocRef)
    
    request = AWSRequest(method='POST', url=hldocrefendpoint, data=ipayload, headers=headershl)
    SigV4Auth(boto3.Session().get_credentials(), service, region).add_auth(request)    
    session = URLLib3Session()
            
    request_result = session.send(request.prepare())
    
    print('lake request result:')
    print(request_result.text)