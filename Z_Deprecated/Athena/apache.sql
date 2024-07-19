CREATE EXTERNAL TABLE IF NOT EXISTS `apache_servers`.`logs` (`host` string, `method` string, `code` string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES ('field.delim' = ',')
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://sooper-dooper-apache-logs-002/logs/'
TBLPROPERTIES ('classification' = 'csv');