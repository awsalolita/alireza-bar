# Task 2 
# Clue 1:Where do we start?
Is there a way to search using EC2 instance ID in CloudTrail?

Penalty: 5 points
# Clue 2:Account Security
Who created the suspicious austoscaling group?

Penalty: 6 points
# Clue 3:Solution
We need to start to remove the attackers access by deleting the keys that were exposed to the attacker.

First, let's find the key the attacker was using.

Identify one of the instance IDs for the suspicious EC2 instances from Step 1

Open AWS Console

Select Services then CloudTrail

In the left-hand margin, select "Event History"

Clear the current filter by selecting the "X" to the right of "false"

On the far right (under Custom) click on the gear icon

Scroll down and enable "AWS Access Key"

In the middle change the filter dropdown to "Resource name"

Enter the EC2 instance ID in the search box and press enter

You should see a RunInstances event; click on this

Under "User Name" make note of "AutoScaling". This tell us the EC2 instance was created using an autoscaling group!!

Change the dropdown to "Event name" and the search query to "CreateAutoScalingGroup"

Looking at the "Resource name" column we see three groups: ApplicationServerGroup, WebServerGroup, and something called Productionz-ProductionLC

Now let us try to find who created the suspicious autoscaling group.

You will have several entries. Select each entry and look for something similar to:

"requestParameters": { "tags": [ "resourceType": "auto-scaling-group", "resourceId": "Productionz-ProductionASG-tddRFUAPqzmW" ] },

Record the username(s) you discovered. You should have discovered a username containing "administrator"

Go back to the Event History and change the dropdown to "User name" and post the entry from the previous step into search, then hit enter

It appears the attacker used the administrator account and STS to standup a Cloudformation:CreateStack which created an autoscaling group for EC2!!

Now let's go to Services, IAM (top left of screen)

Under IAM Resources, select Users

Look for the account we identified in CloudTrail and select it

Select Security Credentials

Scroll down to the access key and select the link to make the key inactive

Go to your challenge dashboard and select the Check my progress button

# Task 3: Recovery

# Clue 1:Tips to Start
Checkout CloudWatch Alerts at: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ConsoleAlarms.html

Penalty: 9 points
# Clue 2:Solution
In the search field next to services, look for CloudWatch

On the navigation pane on the left, select Alarms >> In Alarm

Select Create Alarms, then Select Metric

Type in autoscaling into the search field

Choose: Usage then By AWS Resource

Select the checkbox next to Autoscaling then at the bottom right select Select Metric

The environment for this scenario uses two "legitimate" autoscaling groups, each with two EC2 instances; scroll to the bottom and set the Define threshold value to 2 as this is how many autoscaling groups we know are in use by the customer. This will create the condition ResourceCount > 2 for 1 datapoints within 5 minutes.

Note: In a production environment this may be a different metric, so it's always good to know your environment baselines. We are creating an alarm based on autoscaling group count, as the customer may use additional instances/VCPUs in those over time and we don't want to try and limit false positive events.
Select Next

Choose the radio button next to Create a new topic

Under "Email endpoints that will receive the notification…" enter noemail@nosuchemail.abc

Note: I am using this address for lab purposes; you would use your real e-mail address in a production environment
Select Create Topic

Scroll down and choose Next

Name the alarm. I will name mine Unauthorized_ASG, and then choose next

Scroll down and select Create Alarm

Go to your challenge dashboard and select the Check my progress button