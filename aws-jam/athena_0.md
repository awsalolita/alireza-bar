# Task 1
Clue 2:A different kind of shell
It is a shell tool but not AWS CLI. Think of the usual suspect shell tool.

The following article should give a hint about that shell.

Living off the Land: Attackers Leverage Legitimate Tools for Malicious Ends

Penalty: 6 points
Clue 3:Step-by-step instructions
Solution brief:

In general, if you want to analyze CloudTrail logs using Amazon Athena, you can use "Create Athena table" button under the the Event history page in CloudTrail console.

However, this is not always that case. In our case, we don't have access to the CloudTrail console. We only have access to the CloudTrail logs exported to Amazon S3. In this challenge, we will have to run an Amazon Athena query to create a table from the data stored on Amazon S3. Then, we will write an SQL query to manipulate that table.

You can refer to SQL Reference for Amazon Athena documentation for guidances on Amazon Athena syntax and example queries.

Steps:

Use Amazon Athena to create a table from CloudTrail logs. The solution for this task is in the logs of us-east-1 region.

Refer to Creating the Table for CloudTrail Logs in Athena Using Partition Projection section in Query AWS CloudTrail Logs documentation for the guidance on creating Athena table from CloudTrail logs stored in S3 bucket.

Make sure to update the query to refer to the S3 bucket location of CloudTrail logs for us-east-1 region.

If you are still unable to put this query together, go to the S3 bucket that contains the CloudTrail logs under your account [s3://tcorp-logs-XXXXXXX], and look for a file called query_us-east-1.txt. It has the query ready with your S3 bucket name. Just copy and paste it to Amazon Athena console.

Query the useragent field to list all the user agents used.

Narrow the list of useragents filtering based on the eventdate.

Find the legit shell tool using the following query.

Note that cloudtrail_logs_pp_us_east_1 in the following query is the name of the Amazon Athena table you created in step #1 for us-east-1 region CloudTrail logs. Make sure to update it to match your table name.

SELECT count(useragent) AS Hits, useragent
FROM "cloudtrail_logs_pp_us_east_1"
WHERE eventtime LIKE '%2021-03-11%'
GROUP BY DISTINCT useragent
ORDER BY Hits ASC
The tool we are looking for is AWS Tools for PowerShell. PowerShell is well-known for being used by bad actors because it has lots of capabilities and it is built-in in Windows operating systems. It is now available on Linux and MacOS also.
Troubleshooting:

If you get the following error message while executing the query:

SYNTAX_ERROR: line 1:15 Table awsdatacatalog.default.cloudtrail_logs_pp does not exist

Then, make sure you choose the right database in which you created that table as illustrated here.
# Task 5
# Clue 1:Security Assessment
What is the name of the AWS service responsible for doing security assessment?

Penalty: 5 points
# Clue 2:Step-by-step instructions
Steps:

Use Amazon Athena to create a table from CloudTrail Logs. The solution for this task is in the logs of us-east-1 region.

If you are still unable to put this query together, go to the S3 bucket that contains the CloudTrail logs under your account [s3://tcorp-logs-XXXXXXX], and look for a file called query_us-east-1.txt. It has the query ready with your S3 bucket name. Just copy and paste it to Amazon Athena console.
Query the useragent field to list all the user agents used.

Narrow the list of useragents filtering based on the eventdate.

Use the following query to find the answer.

Note that cloudtrail_logs_pp_us_east_1 in the following query is the name of the Amazon Athena table you created in step #1 for us-east-1 region CloudTrail logs. Make sure to update it to match your table name.

SELECT count(useragent) as Hits, useragent
FROM "cloudtrail_logs_pp_us_east_1"
GROUP BY DISTINCT useragent
ORDER BY Hits ASC
Troubleshooting:

If you get the following error message while executing the query:

SYNTAX_ERROR: line 1:15 Table awsdatacatalog.default.cloudtrail_logs_pp does not exist

Then, make sure you choose the right database in which you created that table as illustrated here.