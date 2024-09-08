Many of the settings can be validated without waiting for the replication task to finish. To validate the Subnet group, the Replication instance and the Endpoints, you can test the connection to each of the Endpoints by navigating to the Endpoint, clicking on the Connections tab, clicking Test connections and clicking Run test.

If the connection isn't sucessful:

Ensure that the Replication Instance is in the DbMigrateJam VPC VPC.
The Subnets selected in the Subnet group should be the Public Subnets if you selected the Public access setting. If that setting is unchecked, the replication instance will work no matter which subnet has been selected as it's only for accessing the databases.
Ensure that the Replication Instance is using the Replication-Instance-SG Security Group.
If the connection is successful to both Endpoints, then there may be an issue with the Endpoints.

Make sure that you created a Source Endpoint for the Oracle database and that all the settings are the same as what's on the Output Properties.
Make sure that you created a Target Endpoint for the RDS Aurora MySQL cluster. When selecting the instance, you have to pick between tgtmysqldb1 and tgtmysqldb2. One of the two is the Writer endpoint which means it's the only one you can write to. To determine which to use, navigate to the RDS Console, under Databases, you will see both DB identifier listed and their role to the right.
Lastly, if the Endpoints are configured properly, there is an issue with the Database migration task.

Make sure that only the DMS_SAMPLE Schema is transferred by replacing the % in the Source name.
The LOB column settings should be set to Limited LOB mode with the Maximum LOB size of 32 KB. Although using Full LOB mode with 64KB also works, but is slower.
Validation can be left disabled.
There's no need for a Premigration assessment.
If you are doing multiple tasks, you should Drop tables on target to make sure the target database is clean each time.

Create a replication Subnet Group
Navigate to the AWS Console.
Search for Database Migration Service in the search bar and click on the service name.
In the left panel, click on Subnet groups.
Click Create subnet group.
Name: jamsg
Description: jamsg solution
VPC: DbMigrateJam VPC
In the Add subnets section, select Private Subnet 1 and Private Subnet 2.
Click Create subnet group.
Create a Replication Instance
In the left panel of the Database Migration Service console, click on Replication instances.
Click Create replication instance
Name the replication instance jamri
Instance class: dms.t3.medium
Engine version: 3.5.1
High Availability: Dev or test workload (Single-AZ)
Allocated storage (GiB): 50
Network type: IPv4
Virtual private cloud (VPC) for IPv4: DbMigrateJam VPC
Replication subnet group: jamsg (based on the previous task above).
UNCHECK Public accessible.
Expand Advanced settings
Availability Zone: No Preference
VPC security groups: Replication-Instance-SG. You can leave or remove Default, it doesn't matter.
AWS KMS key: aws/dms
Click Create replication instance. This step will take 15 minutes.
Create Source Endpoint for the Oracle Database
In the left panel of the Database Migration Service console, click on Endpoints.
Click Create endpoint.
Endpoint type: Source endpoint
CHECK Select RDS DB instance
RDS Instance: dmssmpl
Leave all settings as default as they are already correct.
Access to endpoint database: Provide access information manually
Password: Fleshy_gave0Antony
Expand Test endpoint connection (optional)
VPC: DbMigrateJam VPC
Replication instance: jamri (based on the previous task)
Click Run test. The Status will go from testing to sucessful within a minute.
Click Create endpoint
Create Target Endpoint for the Aurora MySQL Database
Navigate to the Relational Database Service (RDS) Console by searching for it in the Search bar and clicking on the service.
Click Databases in the left panel.
Find which of the tgtmysqldb1 or tgtmysqldb2 Aurora MySQL endpoints is the Writer instance. Under Role next to the DB identifier, one of the two will have the role Writer instance. Take a note of which one it is.
Search for Database Migration Service in the search bar and click on the service name.
In the left panel of the Database Migration Service console, click on Endpoints.
Click Create endpoint.
Endpoint type: Target endpoint
CHECK Select RDS DB instance
RDS Instance: select either tgtmysqldb1 or tgtmysqldb2 based on what you found as the
Writer instance in the previous steps.

Leave all settings as default as they are already correct.
Access to endpoint database: Provide access information manually
Password: Bill_strike5patent
Expand Test endpoint connection (optional)
VPC: DbMigrateJam VPC
Replication instance: jamri (based on the previous task)
Click Run test. The Status will go from testing to sucessful within a minute.
Click Create endpoint
Create the Database Migration Task
In the left panel of the Database Migration Service console, click on Database migration tasks.
Click Create task
Task identifier: jamdmt
Replication instance: jamri (based on the previous task)
Source database endpoint: dmssmpl
Target database endpoint: tgtmysqldb1 or tgtmysqldb2 based on what you selected in the previous task.
Migration type: Migrate existing data
Target table preparation mode: Drop tables on target (in case you ran another task before)
LOB column settings: Limited LOB mode
Maximum LOB size (KB): 32
Data Validation: Turn off
CHECK Task logs Turn on CloudWatch logs
In the Table mappings, select Wizard for the Editing mode.
Click Add new section rule
Schema: Enter a schema
Source name: DMS_SAMPLE
Source table name: %
Action: Include
UNCHECK Turn on premigration assessment
Start migration task: Automatically on create. This task will finish under 10 minutes.




