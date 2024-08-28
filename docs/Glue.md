# Create Crawler
* Crawl a s3 bucket or a db
* it makes a data catalog db
* ETL job to convert the data from data catalog to s3, drop columns or other stuff


# Connections
* jdbc
`jdbc:mysql://[HOST]:3306/<database>`
* it can have network options and vpc


# Lake Formation
* revoke 2*`IAMAllowedPrincipals`
* you can give fine grained access to iam users

* you can create filters 
* row filter , to include all `true` in the box

# RDS
* Creatiing connector with the vpc and password configuration
* Add table using crawlers
    * Data source JDBC
    * `<database>/%`
# redshift
* `<database>/<schema>/%`

# Glue Script for OpenSearch
* give job parameters based on these
```python
# The Jobs parameters are received here
args = getResolvedOptions(sys.argv, ["JOB_NAME","es_user","es_pass","es_endpoint","input_bucket"])
```
* specify the parameters and jar file and 
```
s3://ingestion-bucket-833489210809-us-east-1/elasticsearch-hadoop-7.8.0.jar
```

# WorkFlow
* add new trigger
* add `jobs` or `crawler` for trigger