
* create vpc flow logs to s3
* launch athena , change settings to s3 url( go till the day for url)
* in query one

```CREATE EXTERNAL TABLE IF NOT EXISTS default.vpc_flow_logs (
  version int,
  account string,
  interfaceid string,
  sourceaddress string,
  destinationaddress string,
  sourceport int,
  destinationport int,
  protocol int,
  numpackets int,
  numbytes bigint,
  starttime int,
  endtime int,
  action string,
  logstatus string
)
PARTITIONED BY (dt string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
LOCATION 's3://{BUCKET}/AWSLogs/{ACCOUNT_ID}/vpcflowlogs/us-east-1/2024/03/04/10/'
TBLPROPERTIES ("skip.header.line.count"="1");



ALTER TABLE default.vpc_flow_logs
    ADD PARTITION (dt='YYYY-MM-DD')
    location 's3://{BUCKET}/AWSLogs/{ACCOUNT_ID}/vpcflowlogs/us-east-1/2024/03/04/10/';


SELECT day_of_week(from_iso8601_timestamp(dt)) AS
     day,
     dt,
     interfaceid,
     sourceaddress,
     destinationport,
     action,
     protocol
   FROM vpc_flow_logs
   WHERE action = 'REJECT' AND protocol = 6
   order by sourceaddress
   LIMIT 100;
```