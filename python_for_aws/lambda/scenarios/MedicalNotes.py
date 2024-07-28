#
import boto3
import os
import time

# Set up boto clients and environment variables
s3 = boto3.client('s3')
translate = boto3.client('translate')
comprehendmedical  = boto3.client('comprehendmedical')
outputBucket = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    record = event['Records'][0]
    
    bucket = record['s3']['bucket']['name']	
    s3object = record['s3']['object']['key']
    outputObj = s3object +time.strftime("%Y%m%d_%H%M%S")+'.csv'
    content = "File,Text,Category,Type,Score\n"

    print('processing file : ' + s3object)
    data = s3.get_object(Bucket=bucket, Key=s3object)
    textToTranslate = data['Body'].read().decode('utf-8') 
    english = translate.translate_text(Text=textToTranslate, SourceLanguageCode="auto", TargetLanguageCode="en")
    sourceLang = str(english['SourceLanguageCode'])
    entities = comprehendmedical.detect_entities(Text = str(english['TranslatedText']) )
    entity_str=entities['Entities']
				
    for row in entity_str:
        line = s3object+','+row['Text']+','+row['Category']+','+row['Type']+','+str(row['Score'])+'\n'
        content = content + line
        
    print(content)
    
    s3.put_object(Bucket=outputBucket, Key=outputObj, Body=content)
    preURL = s3.generate_presigned_url('get_object', Params = {'Bucket': outputBucket, 'Key': outputObj}, ExpiresIn = 300)
    textResponse = "Translation Complete. \n\nAccess translated file at: \n"+preURL
    results = {"statusCode": 200, "body": textResponse}
    return(results)
    