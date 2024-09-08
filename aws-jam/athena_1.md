# Task 1
Clue 1:Use Athena to query CloudTrail logs in S3
Use Athena to query CloudTrail logs in S3

The secret blueprint was stored in several S3 Buckets with the prefix dark-forrest-assets
List only IAM Users
The CloudTrail userIdentity element contains the information you are looking for:
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html
The reference to assist you building Athena queries:
https://docs.aws.amazon.com/athena/latest/ug/ddl-sql-reference.html
S3 API call reference:
https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html
Penalty: 2 points
Clue 2:First Athena query
Go to the Athena console, make sure Investigator is the selected workgroup
This is the first query to get you started:

-- Lists IAM Users accessing S3 using GetObject and PutObject actions
SELECT useridentity.username as user, requestparameters
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (eventname = 'GetObject'
      OR eventname = 'PutObject')
      AND useridentity.type = 'IAMUser'
GROUP BY  useridentity.username, requestparameters
ORDER BY user;
Penalty: 3 points
Clue 3:Complete walkthrough
The secret blueprint was stored in several S3 Buckets with the prefix dark-forrest-assets
List only IAM Users
The CloudTrail userIdentity element contains the information you are looking for:
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html
The reference to assist you building Athena queries:
https://docs.aws.amazon.com/athena/latest/ug/ddl-sql-reference.html
S3 API call reference:
https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html
Go to the Athena console, make sure Investigator is the selected workgroup.
Run each query in order and analyze results.

The answer is 4

-- Lists IAM Users accessing S3 using GetObject and PutObject actions
SELECT useridentity.username as user, requestparameters
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (eventname = 'GetObject'
      OR eventname = 'PutObject')
      AND useridentity.type = 'IAMUser'
GROUP BY  useridentity.username, requestparameters
ORDER BY user;

user	requestparameters
granny	{"bucketName":"dark-forrest-assets-734","Host":"dark-forrest-assets-734.s3.amazonaws.com","key":"gingerbreadhouse"}
granny	{"bucketName":"dark-forrest-assets-352","Host":"dark-forrest-assets-352.s3.amazonaws.com","key":"gingerbreadhouse"}
granny	{"bucketName":"dark-forrest-assets-543","Host":"dark-forrest-assets-543.s3.amazonaws.com","key":"gingerbreadhouse"}
granny	{"bucketName":"dark-forrest-assets-673","Host":"dark-forrest-assets-673.s3.amazonaws.com","key":"gingerbreadhouse"}
granny	{"bucketName":"dark-forrest-assets-903","Host":"dark-forrest-assets-903.s3.amazonaws.com","key":"gingerbreadhouse"}
granny	{"bucketName":"dark-forrest-assets-194","Host":"dark-forrest-assets-194.s3.amazonaws.com","key":"gingerbreadhouse"}
gretel	{"bucketName":"dark-forrest-assets-734","Host":"dark-forrest-assets-734.s3.amazonaws.com","key":"gingerbreadhouse"}
gretel	{"bucketName":"dark-forrest-assets-194","Host":"dark-forrest-assets-194.s3.amazonaws.com","key":"gingerbreadhouse"}
gretel	{"bucketName":"dark-forrest-assets-543","Host":"dark-forrest-assets-543.s3.amazonaws.com","key":"gingerbreadhouse"}
gretel	{"bucketName":"dark-forrest-assets-673","Host":"dark-forrest-assets-673.s3.amazonaws.com","key":"gingerbreadhouse"}
gretel	{"bucketName":"dark-forrest-assets-903","Host":"dark-forrest-assets-903.s3.amazonaws.com","key":"gingerbreadhouse"}
gretel	{"bucketName":"dark-forrest-assets-352","Host":"dark-forrest-assets-352.s3.amazonaws.com","key":"gingerbreadhouse"}
hansel	{"bucketName":"dark-forrest-assets-352","Host":"dark-forrest-assets-352.s3.amazonaws.com","key":"gingerbreadhouse"}
hansel	{"bucketName":"dark-forrest-assets-194","Host":"dark-forrest-assets-194.s3.amazonaws.com","key":"gingerbreadhouse"}
hansel	{"bucketName":"dark-forrest-assets-734","Host":"dark-forrest-assets-734.s3.amazonaws.com","key":"gingerbreadhouse"}
hansel	{"bucketName":"dark-forrest-assets-673","Host":"dark-forrest-assets-673.s3.amazonaws.com","key":"gingerbreadhouse"}
hansel	{"bucketName":"dark-forrest-assets-903","Host":"dark-forrest-assets-903.s3.amazonaws.com","key":"gingerbreadhouse"}
hansel	{"bucketName":"dark-forrest-assets-543","Host":"dark-forrest-assets-543.s3.amazonaws.com","key":"gingerbreadhouse"}
wolf	{"bucketName":"dark-forrest-assets-543","Host":"dark-forrest-assets-543.s3.amazonaws.com","key":"gingerbreadhouse"}
wolf	{"bucketName":"dark-forrest-assets-673","Host":"dark-forrest-assets-673.s3.amazonaws.com","key":"gingerbreadhouse"}
wolf	{"bucketName":"dark-forrest-assets-734","Host":"dark-forrest-assets-734.s3.amazonaws.com","key":"gingerbreadhouse"}
wolf	{"bucketName":"dark-forrest-assets-194","Host":"dark-forrest-assets-194.s3.amazonaws.com","key":"gingerbreadhouse"}
wolf	{"bucketName":"dark-forrest-assets-352","Host":"dark-forrest-assets-352.s3.amazonaws.com","key":"gingerbreadhouse"}
wolf	{"bucketName":"dark-forrest-assets-903","Host":"dark-forrest-assets-903.s3.amazonaws.com","key":"gingerbreadhouse"}

-- Same as above plus extration of S3 Bucket names using presto functions
SELECT useridentity.username as user, json_extract_scalar(requestparameters, '$.bucketName') AS bucketname
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (eventname = 'GetObject'
      OR eventname = 'PutObject')
      AND useridentity.type = 'IAMUser'
GROUP BY  useridentity.username, json_extract_scalar(requestparameters, '$.bucketName')
ORDER BY user;

user	bucketname
granny	dark-forrest-assets-543
granny	dark-forrest-assets-673
granny	dark-forrest-assets-903
granny	dark-forrest-assets-194
granny	dark-forrest-assets-352
granny	dark-forrest-assets-734
gretel	dark-forrest-assets-734
gretel	dark-forrest-assets-543
gretel	dark-forrest-assets-352
gretel	dark-forrest-assets-903
gretel	dark-forrest-assets-194
gretel	dark-forrest-assets-673
hansel	dark-forrest-assets-673
hansel	dark-forrest-assets-194
hansel	dark-forrest-assets-352
hansel	dark-forrest-assets-543
hansel	dark-forrest-assets-734
hansel	dark-forrest-assets-903
wolf	dark-forrest-assets-194
wolf	dark-forrest-assets-543
wolf	dark-forrest-assets-903
wolf	dark-forrest-assets-673
wolf	dark-forrest-assets-734
wolf	dark-forrest-assets-352

-- Lists only the IAM User names
SELECT useridentity.username as user
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (eventname = 'GetObject'
      OR eventname = 'PutObject')
      AND useridentity.type = 'IAMUser'
      AND json_extract_scalar(requestparameters, '$.bucketName') LIKE 'dark-forrest-assets%'
GROUP BY  useridentity.username
ORDER BY user;

user
granny
gretel
hansel
wolf

# Task 2: EC2 PRIVATE IP
Clue 1:Use Athena to query CloudTrail and VPC Flow logs in S3
Correlate CloudTrail source IP addresses with VPC Flow logs.
The VPC Flow Logs schema:
https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records
The CloudTrail sourceIPAddress element is one of the pieces of the puzzle:
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html
Penalty: 2 points
Clue 2:First Athena query
Go to the Athena console, make sure Investigator is the selected workgroup
This is the first query to get you started:
-- Find all IP addresses used by Hansel and Gretel to make API calls
SELECT DISTINCT sourceipaddress
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (useridentity.username = 'hansel'
        OR useridentity.username = 'gretel');
Penalty: 3 points
Clue 3:Complete walkthrough
Correlate CloudTrail source IP addresses with VPC Flow logs.
The VPC Flow Logs schema:
https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records
The CloudTrail sourceIPAddress element is one of the pieces of the puzzle:
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html
Let's assume Hansel or Gretel have accessed the AWS API and the EC2 instance using the same public IP address.
Query all source IP addresses used by Hansel and Gretel to access the AWS API.
With the response from the previous query, check if there are related VPC Flow Logs matching SSH traffic.
Go to the Athena console, make sure Investigator is the selected workgroup. https://docs.aws.amazon.com/athena/latest/ug/workgroups-create-update-delete.html#switching-workgroups
Run each query in order and analyze results.
The answer is 172.31.44.47 as it was the destination for TCP/22 (SSH) from the public IP addresses used for API calls by Hansel and Gretel

-- Find all IP addresses used by Hansel and Gretel to make API calls
SELECT DISTINCT sourceipaddress
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (useridentity.username = 'hansel'
        OR useridentity.username = 'gretel');
sourceipaddress
107.22.103.105
194.187.249.28

-- Find all IP addresses in VPC Flow logs used for API calls    
SELECT DISTINCT action,
         sourceaddress,
         destinationaddress,
         protocol,
         destinationport,
         numpackets,
         numbytes
FROM "bigwolfdatabase"."vpcflowtable"
WHERE (sourceaddress = '107.22.103.105'
        OR sourceaddress = '194.187.249.28')
ORDER BY numbytes DESC;
action	sourceaddress	destinationaddress	protocol	destinationport	numpackets	numbytes
ACCEPT	194.187.249.28	172.31.44.47	6	22	1053	57708
ACCEPT	194.187.249.28	172.31.44.47	6	22	849	47056
ACCEPT	194.187.249.28	172.31.44.47	6	22	759	39472
ACCEPT	194.187.249.28	172.31.44.47	6	22	604	37764
ACCEPT	194.187.249.28	172.31.44.47	6	22	289	19093
ACCEPT	194.187.249.28	172.31.44.47	6	22	358	18652
ACCEPT	194.187.249.28	172.31.44.47	6	22	256	17728
ACCEPT	194.187.249.28	172.31.44.47	6	22	69	16225
ACCEPT	194.187.249.28	172.31.44.47	6	22	244	14952
ACCEPT	194.187.249.28	172.31.44.47	6	22	34	5685
ACCEPT	194.187.249.28	172.31.44.47	6	22	30	4377
ACCEPT	194.187.249.28	172.31.44.47	6	22	49	3496
ACCEPT	194.187.249.28	172.31.44.47	6	22	13	2277
ACCEPT	194.187.249.28	172.31.44.47	6	22	17	2100
ACCEPT	194.187.249.28	172.31.44.47	6	22	26	1872

NOTE: In this specific scenario, the public IP addresses used for AWS API and ssh into the EC2 instance are the same, but that might not be observed in other cases.

# Task 3: USERS PUBLIC IP
Clue 2:First Athena query
Go to the Athena console, make sure Investigator is the selected workgroup
This is the first query to get you started:
-- Query CloudTrail logs for the sourceIPAddress element used by Hansel and Gretel
SELECT DISTINCT sourceipaddress,
         eventname,
         useragent,
         useridentity.username,
         requestparameters
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (useridentity.type = 'IAMUser'
        AND (eventname = 'GetObject'
        OR eventname = 'PutObject')
        AND (useridentity.username = 'hansel'
        OR useridentity.username = 'gretel'))
ORDER BY  useridentity.username ASC;
Penalty: 3 points
Clue 3:Complete walkthrough
Every CloudTrail event record contains the sourceIPAddress of the request:
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html
Look for CloudTrail event records that represent the relevant S3 Object access pattern:
https://docs.aws.amazon.com/AmazonS3/latest/dev/cloudtrail-logging.html
The CloudTrail userIdentity element is of interest:
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html
Query CloudTrail for GetObject and PutObject activity.
Exclude the User Agent from calls made to the AWS API from the EC2 instance.
The User Agent of the EC2 instance contains this string 4.14.173-137.229.amzn2.x86_64
Go to the Athena console, make sure Investigator is the selected workgroup. https://docs.aws.amazon.com/athena/latest/ug/workgroups-create-update-delete.html#switching-workgroups
Run each query in order and analyze results.

The answer is 194.187.249.28

-- Query CloudTrail logs for the sourceIPAddress element used by Hansel and Gretel
SELECT DISTINCT sourceipaddress,
         eventname,
         useragent,
         useridentity.username,
         requestparameters
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (useridentity.type = 'IAMUser'
        AND (eventname = 'GetObject'
        OR eventname = 'PutObject')
        AND (useridentity.username = 'hansel'
        OR useridentity.username = 'gretel'))
ORDER BY  useridentity.username ASC;

# Task 4
Clue 2:First Athena query
Baseline the requests against S3 Objects and try to find deviations.
A few relevant records to get started, but you will need more than this to resolve this task: eventsource, eventname, useridentity.type.
Use this query to get started:
SELECT eventname,
       useridentity.type,
       count(eventid) as total
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE eventsource = 's3.amazonaws.com'
GROUP BY eventname, useridentity.type
ORDER BY total DESC;
Penalty: 3 points
Clue 3:Complete walkthrough
Every CloudTrail event record contains the sourceIPAddress of the request:
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html
Look for CloudTrail event records that represent the relevant S3 Object access pattern:
https://docs.aws.amazon.com/AmazonS3/latest/dev/cloudtrail-logging.html
Baseline the requests against S3 Objects and try to find deviations.
A few relevant records to get started, but you will need more than this to resolve this task: eventsource, eventname, useridentity.type.
Go to the Athena console, make sure Investigator is the selected workgroup. https://docs.aws.amazon.com/athena/latest/ug/workgroups-create-update-delete.html#switching-workgroups
Run each query in order and analyze results.

The answer is 64.137.178.107

-- S3 access pattern based on type of authentication
SELECT eventname,
       useridentity.type,
       count(eventid) as total
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE eventsource = 's3.amazonaws.com'
GROUP BY eventname, useridentity.type
ORDER BY total DESC;

As you look through the results of the query, you will notice the use of AssumedRole in the element useridentity.type which stands out. All activity is either using IAM User Access Keys or performed by an AWS Service, except for the ListBuckets and GetObject calls coming from a role.

# task 5
Clue 2:First Athena query
Go to the Athena console, make sure Investigator is the selected workgroup
This is the first query to get you started:
-- Query CloudTrail logs for the useridentity element
SELECT useridentity
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE eventsource = 's3.amazonaws.com' AND
      useridentity.type = 'AssumedRole';

It is not useridentity.arn, which is the EC2 instance profile role.


Penalty: 9 points
Clue 3:Complete walkthough
CLUE3 Complete walkthrough

The CloudTrail userIdentity element contains the information you are looking for:
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html
The reference to assist you building Athena queries:
https://docs.aws.amazon.com/athena/latest/ug/ddl-sql-reference.html
S3 API call reference:
https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html
Go to the Athena console, make sure Investigator is the selected workgroup. https://docs.aws.amazon.com/athena/latest/ug/workgroups-create-update-delete.html#switching-workgroups
Run each query in order and analyze results.

The answer is arn:aws:iam::833190257080:role/EC2_S3_ROLE

SELECT DISTINCT useridentity
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE eventsource = 's3.amazonaws.com' AND
      useridentity.type = 'AssumedRole';

useridentity
{type=AssumedRole, principalid=AROA4D7QCMG4DYN7MGA25:i-0c29d6abb6a09589a, arn=arn:aws:sts::833190257080:assumed-role/EC2_S3_ROLE/i-0c29d6abb6a09589a, accountid=833190257080, invokedby=null, accesskeyid=ASIA4D7QCMG4M3U7HEOS, username=null, sessioncontext={attributes={mfaauthenticated=false, creationdate=2020-04-12T20:14:55Z}, sessionissuer={type=Role, principalid=AROA4D7QCMG4DYN7MGA25, arn=arn:aws:iam::833190257080:role/EC2_S3_ROLE, accountid=833190257080, username=EC2_S3_ROLE}}} {type=AssumedRole, principalid=AROA4D7QCMG4DYN7MGA25:i-0c29d6abb6a09589a, arn=arn:aws:sts::833190257080:assumed-role/EC2_S3_ROLE/i-0c29d6abb6a09589a, accountid=833190257080, invokedby=null, accesskeyid=ASIA4D7QCMG4IW4RPPHK, username=null, sessioncontext={attributes={mfaauthenticated=false, creationdate=2020-04-12T21:14:47Z}, sessionissuer={type=Role, principalid=AROA4D7QCMG4DYN7MGA25, arn=arn:aws:iam::833190257080:role/EC2_S3_ROLE, accountid=833190257080, username=EC2_S3_ROLE}}}


As you look through the results and check the CloudTrail documentation for the element useridentity, you will find the ARN of the role used by the EC2 instance profile to be present at useridentity.sessioncontext.sessionissuer.arn


SELECT DISTINCT useridentity.sessioncontext.sessionissuer.arn
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE eventsource = 's3.amazonaws.com' AND
      useridentity.type = 'AssumedRole';

# task 6
Clue 2:You got everything you need
From task 4 you figured out the public IP address used by the actor: 64.137.178.107
From task 2 you figured out the private IP address assigned to the compromised EC2 instance: 172.31.44.47
Penalty: 9 points
Clue 3:Complete walkthrough
The reference to assist you building Athena queries:
https://docs.aws.amazon.com/athena/latest/ug/ddl-sql-reference.html
The VPC Flow Logs schema:
https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records
From task 4 you figured out the public IP address used by the actor: 64.137.178.107
From task 2 you figured out the private IP address assigned to the compromised EC2 instance: 172.31.44.47

The answer is 8080

SELECT *
FROM vpcflowtable
WHERE (sourceaddress = '64.137.178.107' AND
       destinationaddress = '172.31.44.47');