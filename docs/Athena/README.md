### Query a Struct Array ( contians json)
* unnest the array
```sql
SELECT
   name , mydata.high_score as score
FROM
    "games-data-db"."raw_data_053635909469_1b37ced0",
    UNNEST(game_details) as t(mydata)

```
```sql
SELECT
   name , sum(mydata.high_score) as score
FROM
    "games-data-db"."raw_data_053635909469_1b37ced0",
    UNNEST(game_details) as t(mydata)
where name = 'Kayla Douglas'
group by name
```
### Readfrom a csv 
```sql
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
```sql
CREATE TABLE AwsDataCatalog.glue_ticket_db.requests
WITH (
        external_location = 's3://<DATA_LAKE_BUCKET_NAME>/requests'
        )
        
AS SELECT *
FROM "glue-etl-ticket-table";
```

### CloudTrail
* [create table](./CloudTrailCreateTable.sql)
```sql
SELECT useridentity.username as user, requestparameters
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (eventname = 'GetObject'
      OR eventname = 'PutObject')
      AND useridentity.type = 'IAMUser'
GROUP BY  useridentity.username, requestparameters
ORDER BY user;
```
```sql
SELECT useridentity.username as user, requestparameters
FROM "bigwolfdatabase"."cloudtrailtable"
WHERE (eventname = 'GetObject'
      OR eventname = 'PutObject')
      AND useridentity.type = 'IAMUser'
GROUP BY  useridentity.username, requestparameters
ORDER BY user;
```

* useragent cloudtrail
```sql
SELECT count(useragent) as Hits, useragent
FROM "cloudtrail_logs_pp_us_east_1"
GROUP BY DISTINCT useragent
ORDER BY Hits ASC
```
