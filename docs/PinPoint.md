# Integrate with different channels
* send email 
* sms and voice

# Send voice msg
```python
ssml_message = (
    "<speak>"
    "" + message + ""
    "</speak>")

sms_voice_client.boto3.client('pinpoint-sms-voice')
response = sms_voice_client.send_voice_message(
    DestinationPhoneNumber=destination_number,
    OriginationPhoneNumber=origination_number,
    #CallerId=caller_id,phonemeCode
    Content={
        'SSMLMessage': {
            'LanguageCode': language_code,
            'VoiceId': voice_id,
            'Text': ssml_message}})
```