# Clue 1:SNS Topic permissions
Modify the SNS Topic to permit the S3 NOC bucket to publish messages

Refer https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html section IAM policy for a destination SNS topic for permissions required


# Clue 2:KMS permissions
The IMF's SNS topic is encrypted you must grant the Amazon S3 service principal permission to work with the encrypted topics or queue.

Refer https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html section AWS KMS key policy

# Clue 3:S3 Event Notifications
Modify the S3 NOC bucket to enable Event notifications to SNS Topic

Refer https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html for steps to follow to enable S3 event notifications


# Clue 4:Complete Walkthrough
Search for and go to the Simple Notification Service (SNS) console

Click on your topic_NOC_event from the Topics list

Edit the topic and scroll down to Access policy section JSON editor

The "Statement": element already has existing entry, and we need to make additional entry here

On 3rd from last line, just above the "]", you should see a "}"

Add a comma and enter the below new statement and save your changes. Remember to replace X's with your AWS Account number and R's with your AWS Region example us-west-1

    {
      "Sid": "Permit S3 to SNS topic publish policy",
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": "SNS:Publish",
      "Resource": "arn:aws:sns:RR-RRRR-R:XXXXXXXXXXXX:topic_NOC_event",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "XXXXXXXXXXXX"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:*:*:secret-noc-bucket-XXXXXXXXXXXX"
        }
      }
    }
Now search for KMS and in the KMS console go to the customer managed key

Edit the Key policy to add below new statement on line 5

        {
            "Sid": "S3 to use KMS Key",
            "Effect": "Allow",
            "Principal": {
                "Service": "s3.amazonaws.com"
            },
            "Action": [
                "kms:GenerateDataKey",
                "kms:Decrypt"
            ],
            "Resource": "*"
        },
Now come back to the S3 console and go to Properties tab of your S3 NOC bucket

Scroll down to Event notifications and click Create event notification

In the General configuration enter the Event name as IMF_NOC_Event

Under the Event Types select the checkbox for

All object create events
All object remove events
Under the Destination select radio button for SNS topic and from the drop down list select topic_NOC_event and Save your changes

Once the page reloads then click on the Objects tab and upload your NOC_YYYYMMDD.TXT file

On sucessfull upload or remove file you should get email notification