# Task 1: Build ETL jobs in EKS
### Clue 1:Code in Jupyter Notebook
Follow instructions in Jupyter Notebook and run each cell to test the ETL job. The missing block in Jupyter Notebook is:
{
"type": "TypingTransform",
"name": "apply table schema to CSV",
"environments": ["dev", "test"],
"schemaURI": "s3a://"${ETL_CONF_DATALAKE_LOC}"/app_code/meta/contact_meta_0.json",
"inputView": "cdc_raw",            
"outputView": "cdc_typed",
"authentication": {
   "method": "AmazonIAM"
 }
}

### Clue 2 , 3 :Query in Athena console
Query the table in Athena console. Find a column that indicates a record status after a new incremental data change is applied.

Count how many records that are currently invalid.

You have to follow instructions in Jupyter Notebook and run each cell to test the ETL job. The missing block in Jupyter Notebook is:

{
"type": "TypingTransform",
"name": "apply table schema to CSV",
"environments": ["dev", "test"],
"schemaURI": "s3a://"${ETL_CONF_DATALAKE_LOC}"/app_code/meta/contact_meta_0.json",
"inputView": "cdc_raw",            
"outputView": "cdc_typed",
"authentication": {
   "method": "AmazonIAM"
 }
}
When querying in Athena console, you have to find a column that indicates a record status after a new incremental data change is applied. Then, count how many records that are currently invalid. For example, you can write the SQL query in Athena

SELECT count(*) from YOUR_TABLE WHERE iscurrent=0