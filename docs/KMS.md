# give access to role
```json
{
    "Sid": "Allow to encrypt/decrypt using the key",
    "Effect": "Allow",
    "Principal": {
        "AWS": "<RoleArn>"
    },
    "Action": [
        "kms:DescribeKey",
        "kms:Decrypt"
    ],
    "Resource": "*"
}
```

# give access to another account 
[in dms](./DMS.md)

# manual encryption
* get `plaintext` and `ciphertextblob`
```bash
aws kms generate-data-key --key-id alias/myKMSKey --key-spec AES_256 --encryption-context project=practice --region us-east-1 
```
* openssl to encrypt with the plaintext key
```bash
openssl enc -e -aes256 -in samplesecret.txt -out encryptedSecret.txt -k fileb://datakeyPlainText.txt
```
* delete the plaintext file from memory and get another
```bash
aws kms decrypt --encryption-context project=practice --ciphertext-blob fileb://datakeyEncrypted.txt --region us-east-1
```
* decrypt with new plaintext
```bash
openssl enc -d -aes256 -in encryptedSecret.txt -k fileb://datakeyPlainText.txt
```
## direct encrypt
```bash
aws kms encrypt --key-id alias/myKMSKey --plaintext fileb://NewSecretFile.txt --encryption-context project=practice --output text  --query CiphertextBlob --region=us-east-1 | base64 --decode > NewSecretsEncryptedFile.txt
aws kms decrypt --ciphertext-blob fileb://NewSecretsEncryptedFile.txt --encryption-context project=practice --output text --query Plaintext --region=us-east-1 | base64 --decode > NewSecretsDecryptedFile.txt
```

# Sign a request with asymmetric key
```python
raw_data = event['body']
response = kms_client.sign(
        KeyId=sign_kms_id,
        Message=raw_data,
        MessageType='RAW',
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256')
logger.info('Sigature generated for the message body.')
logger.info(response['Signature'])
## Encode the signature to base64. 
sigB64 = base64.urlsafe_b64encode(response['Signature'])
encoded_signature = sigB64.decode("utf-8")
logger.info('Encoded_signature.')
logger.info(encoded_signature)   
signedJWT = f'{raw_data}.{encoded_signature}'
headers = {'Content-Type': 'application/json'}
data = {"jwtData": signedJWT}
logger.info('Data with encoded signature.')
logger.info(data)
```