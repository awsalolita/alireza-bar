### Readfrom a csv 
```
create database mydb;

CREATE EXTERNAL TABLE mydb.mytable (
  `File` string,
  `Text` string,
  `Category` string,
  `Type` string,
  `Score` string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
LOCATION 's3://output-bucket-c3fb0700/'
TBLPROPERTIES ("skip.header.line.count"="1");

```

### Create external table in a s3
```
CREATE TABLE AwsDataCatalog.glue_ticket_db.requests
WITH (
        external_location = 's3://<DATA_LAKE_BUCKET_NAME>/requests'
        )
AS SELECT *
FROM "glue-etl-ticket-table";
```