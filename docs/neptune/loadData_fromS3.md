* create iam role and change trustpolicy for rds
* attach role to neptune cluster 
* export url=neptune-cluster.cluster-cqdnibzb3baa.us-east-1.neptune.amazonaws.com:8182
* curl -X POST -H 'Content-Type: application/json' \https://$url/loader -d'
{
"source": "s3://<BUCKET_NAME>/neptune-data.rdf",
"format": "ntriples",
"iamRoleArn": "<ROLE_ARN>",
"region": "us-east-1",
"failOnError": "FALSE",
"parallelism": "MEDIUM",
"queueRequest": "TRUE"
}'

* Copy the loadID (from the 200 OK message) and monitor the progress of the job using the loadID:

curl -G https://$url/loader/<LOAD ID>

```
Download the RDF4J client:

git clone https://github.com/linuxacademy/content-aws-database-specialty.git
Move into the S06_Additional Database Services directory:

cd content-aws-database-specialty/S06_Additional\ Database\ Services/
Extract the client:

tar -xzvf eclipse-rdf4j-3.4.1-nowar.tgz
Move into the client directory:

cd eclipse-rdf4j-3.4.1
View the console script in the bin directory:

bin/console.sh
Create a SPARQL repo:

create sparql
Specify our endpoint names. Be sure to replace the endpoints with your own, while adding :8182/sparql on the end.

https://<INSERT_NEPTUNE_READER_ENDPONT_HERE>:8182/sparql
Enter the same line after SPARQL update endpoint.

Specify the local repository ID as neptune.

Specify the repository title Neptune Db Instance.

Enter yes to overwrite the existing configuration, if prompted. If successful, a repository created message appears.

Open the repo to view the submitted S3 bucket data:

open neptune
Query the data:

sparql SELECT * where {?s ?p ?o}
This should let you successfully query the data.
```