# Design step function
* Parameters
```json
"Parameters": {
                "BucketName.$": "$.bucket_name",
                "InputFile.$": "$.BatchNumber",
                "OutputFolder.$": "$.output_folder",
              }
```
* input
```json
{
    "bucket_name": "resource-bucket-xxxxx-175",
    "input_file": "input/sample_portfolio.json",
    "output_folder": "output"
  }
```

* if you want to reference another variable in your json , at the end of the key needs `.$` and in value `$.detail.object`
* your lambda should have use `state input as payload`
```json
{
  "Input.$": "$"
}
```
* in the output you can untick `Filter output with OutputPath`

# Choice state
* `$.Payload.status` is equal to `available`




# configs
### Pass state
* the `$` contains all of the input , use this to get a key `$.detail.object.key`
* in a state `Pass state` by default the input goes to the output
* you can `Transform input with parameters` like this
```json
{
  "object.$": "$.detail.object.key"
}
```
### lambda
* choose to use `state input as payload`
* in the output transform the output to make a nice output
```json
{
  "statusCode.$": "$.Payload.statusCode",
  "statusMessage.$": "$.Payload.body.Status",
  "macieJobId.$": "$.Payload.body.JobId",
  "analyticsBucket.$": "$.Payload.body.AnalyticsBucket"
}
```
* By default, it sends task result as output BUT 
* combine the input and output `$.detail.TaskResult`
* this puts the output from lambda to this path `$.detail.TaskResult`
* the output
```json
{
  "bucket2": "cv-analytics-zone-374745590237",
  "bucket1": "cv-ingress-zone-374745590237",
  "object": "00.VPC_4Subnets.yaml",
  "detail": {
    "TaskResult": {
      "analyticsBucket": "cv-analytics-zone-374745590237",
      "macieJobId": "234c66d14dcfc435eab7f94fdc95dbac",
      "statusMessage": "VAULT_COPY",
      "statusCode": 200
    }
  }
}
```
### SNS
* enter a messsage
```json
{
  "Bucket.$": "$.bucket1",
  "Status.$": "$.detail.TaskResult.statusMessage",
  "jobid.$": "$.detail.TaskResult.macieJobId",
  "msg" : "failed dude"
}
```


# Example
```json
"SendToQueue":{
   "Type":"Task",
   "Resource":"arn:aws:states:::sqs:sendMessage",
	 "Next": "IntoDynamoDB",
	 "OutputPath": "$",
	 "ResultPath": "$.queue_response",
	  "Parameters":{
		    "QueueUrl":"REPLACE_WITH_YOUR_QUEUE",
				"MessageBody.$": "$"
		}
}
```

### Glue
* Start job and wait for task to complete
* Start `Crawler`
* output
```json
{
  "AllocatedCapacity": 10,
  "Attempt": 0,
  "CompletedOn": 1724761699143,
  "ExecutionClass": "STANDARD",
  "ExecutionTime": 63,
  "GlueVersion": "2.0",
  "Id": "jr_4fe20407daf538a342b7044dde80a2eceaa37a291dd3512b3cc4c9b27519818f",
  "JobMode": "SCRIPT",
  "JobName": "JSON2Parquet-job",
  "JobRunState": "SUCCEEDED",
  "LastModifiedOn": 1724761699143,
  "LogGroupName": "/aws-glue/jobs",
  "MaxCapacity": 10,
  "NumberOfWorkers": 10,
  "PredecessorRuns": [],
  "StartedOn": 1724761630165,
  "Timeout": 2880,
  "WorkerType": "G.1X"
}
```

* `Get Crawler`, tick add input to output
```
$.response.get_crawler
```
* for the next state to check 
```
$.response.get_crawler.Crawler.State = RUNNING or STOPPING
```
* sample json
```json
{
  "response": {
    "get_crawler": {
      "Crawler": {
        "Classifiers": [],
        "CrawlElapsedTime": 0,
        "CreationTime": "2024-08-27T11:27:54Z",
        "DatabaseName": "shipping-db",
        "LakeFormationConfiguration": {
          "AccountId": "",
          "UseLakeFormationCredentials": false
        },
        "LastCrawl": {
          "LogGroup": "/aws-glue/crawlers",
          "LogStream": "s3_crawler_raw",
          "MessagePrefix": "98df0dba-9f1d-477a-9761-0064151f2425",
          "StartTime": "2024-08-27T12:28:59Z",
          "Status": "SUCCEEDED"
        },
        "LastUpdated": "2024-08-27T11:27:54Z",
        "LineageConfiguration": {
          "CrawlerLineageSettings": "DISABLE"
        },
        "Name": "s3_crawler_raw",
        "RecrawlPolicy": {
          "RecrawlBehavior": "CRAWL_EVERYTHING"
        },
        "Role": "AWSGlueServiceRole-Lab",
        "SchemaChangePolicy": {
          "DeleteBehavior": "DEPRECATE_IN_DATABASE",
          "UpdateBehavior": "UPDATE_IN_DATABASE"
        },
        "State": "READY",
        "Targets": {
          "CatalogTargets": [],
          "DeltaTargets": [],
          "DynamoDBTargets": [],
          "HudiTargets": [],
          "IcebergTargets": [],
          "JdbcTargets": [],
          "MongoDBTargets": [],
          "S3Targets": [
            {
              "Exclusions": [],
              "Path": "s3://staging-bucket-57cfa5d0/transformed_data"
            }
          ]
        },
        "Version": 1
      }
    }
  }
}
```





### Athena 
* Start Query
```json
{
  "QueryString": "SELECT SUM(shipping_cost) AS \"Total_Cost_in_$\",SUM(shipping_distance) AS \"Total_Distance_in_miles\", SUM(quantity) AS \"Total_Fuel_Quantity_in_gal\"  FROM \"shipping-db\".\"transformed_data\";",
  "WorkGroup": "primary"
}
```