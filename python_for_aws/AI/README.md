# Translate (1) (Translates text)
### Translate AutoDetect
```python
english = translate.translate_text(Text=textToTranslate, SourceLanguageCode="auto", TargetLanguageCode="en")
Text = str(english['TranslatedText'])
sourceLang = str(english['SourceLanguageCode'])
```



# Comprehend Medical (2) (Scans medical noskhe)
### Detect Entities
* Entity has `Text` `Category` `Types` `Score`
```python
client = boto3.client('comprehendmedical')
# Deprecated
# entities = comprehendmedical.detect_entities(Text = str(english['TranslatedText']) )
response = comprehend_medical.detect_entities_v2( Text=docText )
data = entities['Entities']
for row in data:
    row['Text']
    row['Category']
    row['Type']
    str(row['Score'])
```

# Textract (3) (extract the text from photos)
* Analyze Document
* Analyze Expense 
* Analyze ID
### Feature Types
* Raw text , form(key value) , query ...
```python
response = textract.analyze_document(    
    Document={                           
        'S3Object': {
            'Bucket': bucket,
            'Name': key
        }
    },
    FeatureTypes=['FORMS',  # FeatureTypes is a list of the types of analysis to perform.
                  ]) 
```
### Extract Text from images (expense)
```python
bucket_name = "mybucket"
file_name = "path/file"Rekognition (5)
textract = boto3.client(service_name='textract', region_name='us-east-1')
response = textract.analyze_expense(Document={'S3Object': {'Bucket': bucket_name, 'Name': file_name}})
fields = response['ExpenseDocuments'][0]['SummaryFields']
for field in fields:
    if field['Type']['Text'] == 'VENDOR_NAME' # EXAMPLE
        # getting the value
        vendor_name = field['ValueDetection']['Text']
    if field['Type']['Text'] == 'TOTAL': #EXAMPLE
        # getting numerical values
        total = Decimal(re.sub('[^0-9.]', '', field['ValueDetection']['Text']))
lineItemGroups = response['ExpenseDocuments'][0]['LineItemGroups']
```
# extract key value with Document (FORM and Table)
```python
# response from textract
response = {}
doc = Document(response)  # You are parsing the textract response using Document.
# The below code reads the Amazon Textract response and
# prints the Key and Value
for page in doc.pages:
    # Print fields
    print("Fields:")
    for field in page.form.fields:
        print("Key: {}, Value: {}".format(field.key, field.value))
        # Search fields by key
        # Enter your code below
        key = "address"
        fields = page.form.searchFieldsByKey(key)
        for field in fields:
            print("Key: {}, Value: {}".format(field.key, field.value))
# The below code reads the Amazon Textract response and
# prints the Table data. Uncomment below to use the code.
for page in doc.pages:
    print("\nTable details:")
    for table in page.tables:
        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                print("Table[{}][{}] = {}".format(r, c, cell.text))
```
# Transcribe (4)
### python transcribe
```python
transcribe_client = boto3.client('transcribe')
file_uri = 's3://'
job_name = 'myjob'
transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp3', #mp4
        LanguageCode='en-US'
    )
```
* get job
```python
transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
```
#### Medical Transcribe
```python
response = client.start_medical_transcription_job(
        MedicalTranscriptionJobName=jobName,
        LanguageCode='en-US',
        MediaFormat='mp3',
        Media={
            'MediaFileUri': s3Path
        },
        OutputBucketName=output_bucket,
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 2,
            'ChannelIdentification': False,
            'ShowAlternatives': False
        },
        ContentIdentificationType='PHI',
        Specialty='PRIMARYCARE',
        Type='CONVERSATION'
    )
```
#### read s3 trigger from a transcribe completion
```python
text = ""
s3.download_file(s3bucket, s3object, local_file_name)
    
f = open (local_file_name, "r")
data = json.loads(f.read())
for transcript in data['results']['transcripts']:
    text = transcript['transcript']
f.close()
```
#### S3 Upload trigger and transcribe the voice message
[here](./Lambda_TranscribeS3Trigger.py)

# Rekognition (5)
* lable detection: tells you about the image , person cars city and ...
* Image moderation: tells you its adult content
* Image properties: colors and shit
* PPE detection: personal protective equipment


```python
rekognition_client = boto3.client('rekognition')
```
* detect label
```python
response_rekognition = rekognition_client.detect_labels(   # You are calling detect_labels API 
    Image={                                                # to analyzing Images Stored in an Amazon S3 Bucket
        'S3Object': {
            'Bucket': bucket,
            'Name': image
        }
    },
    MinConfidence=70                                        # MinConfidence specifies the minimum confidence  
) 
mylabes = response_rekognition['Labels']
```
* Process image from iot event , detect protective equipment
```python
byte = str.encode(event['data'])
# Call Amazon Rekognition
response = rekognition_client.detect_protective_equipment(
     Image={
        'Bytes': base64.b64decode(byte)
    },
    SummarizationAttributes={
        'MinConfidence': 90,
        'RequiredEquipmentTypes': [
            'FACE_COVER'
        ]
    }
)
```

* Detect Safe content
```python
response = rekognition_client.detect_moderation_labels(
        Image={"S3Object": {"Bucket": event['bucket'], "Name": event['key']}})
moderation_labels = response['ModerationLabels'] if 'ModerationLabels' in response else None
if not moderation_labels:
    return {'safe_content': True}
else:
    return {'safe_content': False}

```

# Comprehend (6)
* Detect Sentiments
```python
comprehend_client = boto3.client('comprehend')
sentiment = comprehend_client.detect_sentiment(Text="hello" LanguageCode='en')['Sentiment']
```
* job
```python
response_sentiment_detection_job = comprehend.start_sentiment_detection_job(
            InputDataConfig={
                'S3Uri': f's3://{bucket}/{key}',
                'InputFormat': 'ONE_DOC_PER_LINE',
            },
            OutputDataConfig={
                'S3Uri': f's3://{output_bucket}/output/'
            },
            JobName=job_name,
            LanguageCode='en',
            DataAccessRoleArn=data_arn,
        )
```

# Polly (7)
* text to speech
```python
polly_client = boto3.client('polly')
polly_client.start_speech_synthesis_task( 
                        Engine='neural',
                        LanguageCode="en-US",
                        OutputFormat='mp3',
                        OutputS3BucketName="mybucket",
                        OutputS3KeyPrefix="output/"+"output.mp3",
                        Text="hello dude",
                        TextType='text',
                        VoiceId="Salli"
                        )
```

# Health Lake (8)
### Write
* We need to format the results from comprehend medical to healthlake DocumentReference's extension format
* the whole code [is here](./WriteToHealthLake.py) `DATASTORE_ID` `REGION_ID`
### Read
* [sample read](./ReadFromHealthLake.py) `DATASTORE_ID` `REGION_ID`


# Kendra (9)
* index stuff for searching 
* it has a `datasource` and `index`
```python
kendra_client = boto3.client("kendra")
kendra_client.start_data_source_sync_job(
        Id=KENDRA_DATA_SOURCE_ID, IndexId=KENDRA_INDEX_ID
    )
```