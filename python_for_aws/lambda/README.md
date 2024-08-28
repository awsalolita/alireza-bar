### S3 Trigger, Translate, Comprehend Medical
[Lambda](./scenarios/MedicalNotes.py)    
### POST link, Download&Resize image
link in the `event`     
[Lambda](./sendfile_resizeImage.py)
### get query parameters
```python
event['queryStringParameters']['TheFuckingParameter']
```