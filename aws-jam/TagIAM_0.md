# Task 1: Allow tagging with "jam_testing" only if value is "yes" or "no"
### Clue 1:Where
To complete this task,

Go to the IAM console by going to 'Services' in the top left of the AWS console and selecting 'IAM'.
Select 'Roles' from the options on the left.
Search for 'JAM_DEVELOPER_ROLE' and click to see the details of the role.
Under permissions, you see that the role has one AWS Managed Policy attached to it.
Click on 'Add inline policy'
Create an inline policy with a deny statement
The statement must deny permission to the IAM role to tag an EBS volume if the tag key is 'jam_testing' and the value is not 'yes' or 'no'
### Clue 2:Condition Keys
Click on 'Add Inline Policy' and create the inline policy.
Include a deny statement in the policy to deny access for CreateTags action performed on EBS volumes under specific conditions.
Include the condition key "StringNotEqualsIfExists" for "aws:RequestTag/jam_testing" so that the deny only applies if the value for this tag is set to something other than "yes" or "no".

### Clue 3:Inline policy

To complete task 1,

Go to the IAM console -> from 'Services' in the top left of the AWS console, select 'IAM'.
Select 'Roles' from the options on the left.
Search for 'JAM_DEVELOPER_ROLE' and click to see the details of the role.
Under permissions, you see that the role has one AWS Managed Policy attached to it.
Click on 'Add an inline policy'
In the 'Create Policy' screen, go to the 'JSON' tab.
Replace the sample json with the below json IAM policy.
This policy statement prevents the developer from creating a tag for EBS volumes unless the tag key is "jam_testing" and value is "yes" or "no".
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "JamTask1",
            "Effect": "Deny",
            "Action": "ec2:CreateTags",
            "Resource": [
                "arn:aws:ec2:*:*:volume/*"
            ],
            "Condition": {
                "StringNotEqualsIfExists": {
                    "aws:RequestTag/jam_testing": [
                        "yes",
                        "no"
                    ]
                }
            }
        }
    ]
}
Click "Review Policy"
Give the policy a suitable "Name" and click "Create Policy".