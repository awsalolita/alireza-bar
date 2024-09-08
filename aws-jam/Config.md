# Clue 1:AWS Config
AWS Config provides a detailed view of the configuration of AWS resources in your AWS account. Follow the URL to learn more - https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html

A conformance pack is a collection of AWS Config rules and remediation actions that can be easily deployed as a single entity in an account and a Region or across an organization in AWS Organizations. Follow the URL to learn more - https://docs.aws.amazon.com/config/latest/developerguide/conformance-packs.html

Use the AWS Config Conformance Pack - Operational best practices for Amazon S3 - https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-amazon-s3.html

Penalty: 19 points

# Clue 2:AWS Conformance Packs
To set up AWS Config with the console - https://docs.aws.amazon.com/config/latest/developerguide/gs-console.html

Use the AWS Config Conformance Pack - Operational best practices for Amazon S3 - https://docs.aws.amazon.com/config/latest/developerguide/conformance-pack-console.html#deploy-cpack-using-sample-template

To edit the public read/write access for Amazon S3 bucket using ACLs - https://docs.aws.amazon.com/AmazonS3/latest/userguide/managing-acls.html

To edit public access settings for Amazon S3 bucket - https://docs.aws.amazon.com/AmazonS3/latest/user-guide/block-public-access-bucket.html

To enable versioning for an Amazon S3 bucket - https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-versioning.html

To enable server access logging for an Amazon S3 bucket - https://docs.aws.amazon.com/AmazonS3/latest/user-guide/server-access-logging.html

To add a replication rule to an Amazon S3 bucket - https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-replication.html

To ensure S3 buckets have policies that require requests to use Secure Socket Layer (SSL) - https://aws.amazon.com/premiumsupport/knowledge-center/s3-bucket-policy-for-config-rule/

To enable server-side encryption with AWS KMS for an Amazon S3 bucket - https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html

Penalty: 22 points

# Clue 3:AWS Conformance Pack - Operational best practices for AWS S3
Setting up AWS Config

Open AWS Console, and navigate to AWS Config or open the AWS Config console directly at https://console.aws.amazon.com/config/
Choose Get Started.
On the Settings page, under Recording method, for Recording strategy, select Specific resource types. Under Resource types to record, for Resource type select AWS S3 Bucket and for Frequency, select Continuous.
For IAM role for AWS Config, select Choose a role from your account.
From the Existing roles drop-down menu, select AWSServiceRoleForConfig.
For Amazon S3 Bucket, choose Create a bucket. For Bucket Name, a default name will be auto added by the config and you can leave it like this.
For Amazon SNS Topic, leave it unchecked.
Choose Next.
Do not select any rules and choose Next.
Review the settings, and select Confirm
Deploying AWS Conformance Pack - Amazon S3 Operational best practices

Open AWS Console, and navigate to AWS Config or open the AWS Config console directly at https://console.aws.amazon.com/config/
Navigate to the Conformance packs page and choose Deploy conformance pack.
On the Specify template page, choose a sample template.
Type S3 in the Sample Template drop box to filter the conformance packs, then select Operational Best Practices for Amazon S3
Choose Next.
On the Specify conformance pack details page, type the name for your conformance pack. (Example: ops-best-s3)
Skip the Parameters - optional section.
Choose Next.
On the Review and deploy page, review all of the information.
Choose Deploy conformance pack.
Disclaimer Please resolve the issues manually and do not use Systems Manager Documents for resolving the issues. The end users do not have sufficient permissions to use Systems Manager Document.

To edit the public read/write access for Amazon S3 bucket using ACLs

Open AWS Console, and navigate to S3 console or open the Amazon S3 console directly at https://console.aws.amazon.com/s3/
In the Bucket name list, choose the bucket that you want to edit its ACL settings for public read and write, and then choose the Permissions tab.
In the Access control list (ACL) section, choose Edit.
Under the Everyone (public access) Grantee, deselect all options.
Choose Save changes.
To edit public access settings for Amazon S3 buckets

Open AWS Console, and navigate to S3 console or open the Amazon S3 console directly at https://console.aws.amazon.com/s3/
In the Bucket name list, choose the bucket that you want to edit its public access settings, and then choose the Permissions tab.
In the Block public access (bucket settings) section, choose Edit, then select the top most checkbox Block all public access (this will select the 4 below checkboxes as well), and then choose Save changes.
When you're asked for confirmation, enter confirm. Then choose Confirm to save your changes.
To enable versioning for an Amazon S3 bucket

Open AWS Console, and navigate to S3 console or open the Amazon S3 console directly at https://console.aws.amazon.com/s3/
In the Bucket name list, choose the name of the bucket that you want to enable versioning for.
Choose the Properties tab.
Under the Bucket versioning section, choose Edit.
Select Enable, and then choose Save changes.
To enable server access logging for an Amazon S3 bucket

Open AWS Console, and navigate to S3 console or open the Amazon S3 console directly at https://console.aws.amazon.com/s3/
Choose Create bucket.
Under the Bucket name, enter a unique identifiable name like my-jam-logging-bucket-.
Make sure the region is set to the same region of the challenge.
Choose Create bucket.
In the Buckets list, choose the name of the bucket that you want to enable server access logging for.
Choose the Properties tab.
In the Server access logging section, choose Edit.
Select Enable.
For Target bucket, choose Browse S3 and select the name of the bucket that you created for logging, then choose Choose path.
Choose Save changes.
To add a replication rule to an Amazon S3 bucket

Open AWS Console, and navigate to S3 console or open the Amazon S3 console directly at https://console.aws.amazon.com/s3/
Choose Create bucket.
Under the Bucket name, enter a unique identifiable name like my-jam-replication-bucket-. This bucket will be used as destination bucket for replication.
Make sure the region is to the same region of the challenge. Note: In real world scenario, your source and destination Amazon S3 buckets will be in two different regions but due to restrictions in the AWS JAM environment, we are going to create the source and destination Amazon S3 buckets in the same region.
Under the Bucket versioning section, select Enable.
Choose Create bucket.
In the Buckets list, choose the name of the bucket that you want to enable replication for.
Choose the Management tab, then under the Replication rules section, choose Create replication rule.
In the Create replication rule page, under Replication rule name enter my-rule.
In the Source bucket section, select Apply to all objects in the bucket.
In the Destination section, select Choose a bucket in this account, then choose Browse S3 and select the name of the bucket that you created for replication, then choose Choose path.
In the IAM role section, select Choose from existing IAM roles. Then, in the IAM role drop-down menu, select the given IAM role provided in the Output Properties of this JAM challenge with name as myS3ReplRole.
Choose Save.
Choose Submit.
To ensure S3 buckets have policies that require requests to use Secure Socket Layer (SSL)

Open AWS Console, and navigate to S3 console or open the Amazon S3 console directly at https://console.aws.amazon.com/s3/
In the Bucket name list, choose the name of the bucket that you want to edit its policy.
Choose the Permissions tab, and then in the Bucket Policy section, choose Edit.
In the Bucket policy editor text box, type or copy and paste bucket policy from this reference link (https://aws.amazon.com/premiumsupport/knowledge-center/s3-bucket-policy-for-config-rule/) and edit the name of the bucket in the policy. Note: The bucket policy is a JSON file. The text you type in the editor must be valid JSON.
Choose Save changes.
To enable server-side encryption with AWS KMS for an Amazon S3 bucket

Open AWS Console, and navigate to S3 console or open the Amazon S3 console directly at https://console.aws.amazon.com/s3/
In the Bucket name list, choose the name of the bucket that you want to enable server-side encryption settings for.
Choose the Properties tab.
In the Default encryption section, choose Edit.
For the Encryption key type, select AWS Key Management Service key (SSE-KMS).
For the AWS KMS key, select Choose from your AWS KMS keys.
In the Available AWS KMS keys drop-down menu, select the key ARN that ends with aws/s3. This is the the AWS managed KMS key for S3 encryption.
Choose Save changes.
Notes:

Once you completed all the above steps, the AWS Config Conformance Pack should automatically update the compliance status as Compliant for the selected compliance criteria that you configured. This might take couple of minutes to do so.
The required rules might still show a Noncompliant status for the other buckets in the challenge which should be fine. The goal of the challenge is to make the mys3bucket1 bucket compliant.
There will be other rules in the conformance pack that still shows Noncompliant status but they are not required for this challenge.