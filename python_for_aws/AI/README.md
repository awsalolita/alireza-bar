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
entities = comprehendmedical.detect_entities(Text = str(english['TranslatedText']) )
data = entities['Entities']
for row in data:
    row['Text']
    row['Category']
    row['Type']
    str(row['Score'])
```

# Textract (3) (extract the text from photos)
### Extract Text from images
```python
bucket_name = "mybucket"
file_name = "path/file"
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

# Transcribe
### python transcribe
```python
transcribe_client = boto3.client('transcribe')
file_uri = 's3://'
job_name = 'myjob'
transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )

```
* get job
```python
transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
```

### S3 Upload trigger and transcribe the voice message
[here](./Lambda_TranscribeS3Trigger.py)