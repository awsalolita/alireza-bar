# Iot core
### policy example
```json
IoT policy #1

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish",
        "iot:Subscribe",
        "iot:Receive"
      ],
      "Resource": "arn:aws:iot:us-east-1:*:topic/devices/equipment",
  "Condition": {
        "IpAddress": {
          "aws:SourceIp": "<EC2 Instance Public IP>/32"
        }
      },
    },
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:us-east-1:*:client/${iot:Connection.Thing.ThingName}"
    }
  ]
}

```

### credential
```bash
aws iot create-keys-and-certificate --set-as-active \
--certificate-pem-outfile certs/certificate.pem \
--public-key-outfile certs/public.key \
--private-key-outfile certs/private.key
```
* endpoints
```
aws iot describe-endpoint --endpoint-type iot:CredentialProvider
aws iot describe-endpoint --endpoint-type iot:Data-ATS
```


* RootCA1 -> root-CA.crt
* create a thing (Client ID is the thing name)
### rule
* make a rule for the thing
```sql
select * from 'mytopic'
select * from '#'
SELECT * FROM 'device/+/devicePayload'
SELECT gas_reading FROM 'Device_Simulator/telemetry' WHERE gas_reading > 500
SELECT * FROM 'smart_door/actuator'  WHERE permission="denied"
```
* make a policy to allow *
```
arn:aws:iot:us-west-2:695153691056:topic/device/*/rechargeAlert
```
* s3 rule for the key
```
${topic()}/${timestamp()}
```



### shadow
```json
{
  "state": {
    "desired": {
      "airConditioningIsOn": false
    },
    "reported": {
      "airConditioningIsOn": false
    }
  }
}
```
# rule to kinesis data stream
* needs an iam role
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "kinesis:PutRecord",
                "kinesis:PutRecords"
            ],
            "Resource":"<StreamArn>" ,
            "Effect": "Allow"
        }
    ]
}
```
# Functions
* `topic()` part of a topic ->  '/ali/foo/bar' -> topic(2) = foo
* ${topic(2)} in rule
* 

# greengrass
* update sudo
```bash
sudo cp /etc/sudoers /etc/sudoers.bak
sudo sed -i 's/root\tALL=(ALL)/root\tALL=(ALL:ALL)/g' /etc/sudoers  
```
```bash
systemctl status greengrass.service
```
* Create Deployment
```bash
sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir ~/environment/etl@edge/ggAccel.etl_simple.extract/recipes \
  --artifactDir ~/environment/etl@edge/ggAccel.etl_simple.extract/artifacts \
  --merge "ggAccel.etl_simple.extract=1.0.0"
```
* delete a component from deployment
```
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove com.industryquest.TcpSocketConverter
```
```sql
SELECT * from '<GreengrassQuickStartCore-Name>/etl_simple/load'
```
### Component json
* sample json
```json
{
  "RecipeFormatVersion": "2020-01-25",
  "ComponentName": "ggAccel.etl_simple.extract",
  "ComponentVersion": "1.0.1",
  "ComponentType": "aws.greengrass.generic",
  "ComponentDescription": "ETl Accelerator Extract Function V3.",
  "ComponentPublisher": "Amazon",
  "ComponentConfiguration": {
    "DefaultConfiguration": {
      "topic_extr_pub": "etl_simple/extract",
      "accessControl": {
        "aws.greengrass.ipc.pubsub": {
          "ggAccel.etl_simple.extract:pubsub:1": {
            "policyDescription": "Allows access to publish to all local topics.",
            "operations": ["aws.greengrass#PublishToTopic"],
            "resources": ["*"]
          }
        }
      }
    }
  },
  "Manifests": [
    {
      "Platform": {
        "os": "linux"
      },
      "Lifecycle": {
        "Setenv": {
          "FILE_PATH": "{artifacts:decompressedPath}/ggAccel.etl_simple.extract"
        },
        "Install": "python3 -m pip install -r {artifacts:decompressedPath}/ggAccel.etl_simple.extract/requirements.txt",
        "Run": "python3 -u {artifacts:decompressedPath}/ggAccel.etl_simple.extract/extract.py --publish-topic '{iot:thingName}/{configuration:/topic_extr_pub}'\n"
      },
      "Artifacts": [
        {
          "URI": "s3://component-artifact-ce1a32b0/ggAccel.etl_simple.extract/1.0.1/ggAccel.etl_simple.extract.zip",
          "Unarchive": "ZIP"
        }
      ]
    }
  ],
  "Lifecycle": {}
}

```




