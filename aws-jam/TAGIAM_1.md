Clue 1:Review Condition Keys for EC2 Actions
Note that both the IAM Roles and the EC2 Instances are tagged with the key Project with values Red or Green.

Review the IAM Policy document named 'ManageEC2InstancesWithProjectTag' and see that it has multiple Statements. You need to edit this Policy document to add IAM Condition elements to Statements with Sid starting with '01', '02' and '03' to meet each requirement in this challenge. You don't need to change the Resource or Action elements in the Statements.

Review the available IAM Condition Keys for the EC2 Actions RunInstances, StartInstances and StopInstances to see how you can add a Condition for the tags on the Instance for each action.

Review the Example IAM Policies for EC2 RunInstances with Tags for a sample IAM Policy Document that provides permissions to run EC2 Instances with specific tags.

Review the documentation for the ec2:CreateAction condition that can be used to restrict tagging permissions to the resource-creating actions only.

Penalty: 26 points
Clue 2:Review Global IAM Condition keys
Review Controlling Access for IAM Principals to see how '${aws:PrincipalTag/tagkey}' can be used in a Condition. This will allow you to create an IAM Policy Condition that allows an action when the Instance's resource tag and the tag on an IAM Principal (such as an IAM Role) have the same value for a key (Project in this case).

Review the IAM Condition key aws:TagKeys that can be used define what tag keys are allowed. Use the ForAllValues set operator to enforce that 'Project' is the only tag key allowed for the RunInstances action in the Statement with Sid starting with '02'

Penalty: 30 points
Clue 3:Edit the Policy
Clue 3: Edit the Policy

Go to the IAM Console and choose Policies from the panel on the left.
Type 'project' in the Search field to see policies with project in the name.
Choose the Policy named 'ManageEC2InstancesWithProjectTag'.
Choose Edit Policy and choose the JSON tab to edit the policy document.
Delete the existing policy document and replace it with the following IAM Policy document. Note that this policy document adds Condition elements to the three statements with Sid beginning with 01, 02, and 03:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "01AllowStopStartWithProjectTag",
      "Effect": "Allow",
      "Action": [
        "ec2:StopInstances",
        "ec2:StartInstances"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:instance/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Project": "${aws:PrincipalTag/Project}"
        }
      }
    },
    {
      "Sid": "AllowRunInstancesResourcesNoTags",
      "Effect": "Allow",
      "Action": "ec2:RunInstances",
      "Resource": [
        "arn:aws:ec2:*::image/*",
        "arn:aws:ec2:*:*:subnet/*",
        "arn:aws:ec2:*:*:network-interface/*",
        "arn:aws:ec2:*:*:security-group/*",
        "arn:aws:ec2:*:*:key-pair/*"
      ]
    },
    {
      "Sid": "02AllowRunInstancesWithProjectTag",
      "Effect": "Allow",
      "Action": [
        "ec2:RunInstances"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:instance/*",
        "arn:aws:ec2:*:*:volume/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestTag/Project": "${aws:PrincipalTag/Project}"
        },
        "ForAllValues:StringEquals": {
          "aws:TagKeys": [
            "Project"
          ]
        }
      }
    },
    {
      "Sid": "03AllowCreateTagsOnRunInstances",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateTags"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:instance/*",
        "arn:aws:ec2:*:*:volume/*"
      ],
      "Condition": {
        "StringEquals": {
          "ec2:CreateAction": [
            "RunInstances"
          ]
        }
      }
    }
  ]
}
Choose Review Policy and choose Save changes. If you have more than 5 previous versions you'll see a confirmation box. Leave the default choice selected and choose Delete version and save.
Wait 20 seconds and browse to or refresh the VerifierUri from the Output Properties to see the test results and get the challenge answer.