# Concept
* Creating a `keyspace` and `table` in it  
* Primary and Clustering column

# cqlsh
### Creating keyspace
```sql
python3 -m pip install --user cqlsh-expansion
export AWS_DEFAULT_REGION=us-east-1
cqlsh-expansion.init
cqlsh-expansion cassandra.us-east-1.amazonaws.com 9142 --ssl

CREATE KEYSPACE IF NOT EXISTS "myGSGKeyspace"WITH REPLICATION = {‘class': 'SingleRegionStrategy’};
 
SELECT * FROM system_schema_mcs.keyspaces WHERE keyspace_name = 'myGSGKeyspace’;
USE "myGSGKeyspace";

# Create table
CREATE TABLE IF NOT EXISTS "myGSGKeyspace".employees_tbl (id text,name text,region text,division text,project text,role text,pay_scale int,vacation_hrs float,manager_id text,PRIMARY KEY (id,division)) WITH CLUSTERING ORDER BY (division ASC) ;  

SELECT * from system_schema.tables WHERE keyspace_name='myGSGKeyspace’ ;

SELECT * FROM system_schema.columns WHERE keyspace_name='mykeyspace' AND table_name='mytable';
```
### insert record
```sql
CONSISTENCY LOCAL_QUORUM;

INSERT INTO "myGSGKeyspace".employees_tbl (id, name, project, region, division, role, pay_scale, vacation_hrs, manager_id) VALUES ('0-5678','Russ','NightFlight','US','Engineering','IC',3,12.5, '0-7890') ;

SELECT * FROM "myGSGKeyspace".employees_tbl ;
```
### insert multiple records
```sql
CONSISTENCY LOCAL_QUORUM;
USE "myGSGKeyspace";
COPY employees_tbl (id,name,project,region,division,role,pay_scale,vacation_hrs,manager_id) FROM 'path-to-the-csv-file/employees.csv' WITH delimiter=',' AND header=TRUE ;
SELECT * FROM employees_tbl ;
SELECT name, id, manager_id FROM "myGSGKeyspace".employees_tbl WHERE id='0-7890' ;
UPDATE "myGSGKeyspace".employees_tbl SET pay_scale=5 WHERE id='0-0123' AND division='Marketing' ;
```
* Deleting a cell
```sql
DELETE manager_id FROM "myGSGKeyspace".employees_tbl WHERE id='0-0-2345' AND division='Exe';
```
* Delete rows
```sql
DELETE FROM "myGSGKeyspace".employees_tbl WHERE id='0-9012' AND division='Eng';
```


# AWS cli
* Create KeySpace
```bash
aws keyspaces create-keyspace --keyspace-name myGSGKeyspace --tags key=keyspace,value=AmazonKeyspaces
```

# python
```python
from cassandra.cluster import Cluster

from ssl import SSLContext, PROTOCOL_TLSv1_2 , CERT_REQUIRED

from cassandra.auth import PlainTextAuthProvider

 

ssl_context = SSLContext(PROTOCOL_TLSv1_2 )

ssl_context.load_verify_locations('path_to_file/sf-class2-root.crt')

ssl_context.verify_mode = CERT_REQUIRED

auth_provider = PlainTextAuthProvider(username='ServiceUserName', password='ServicePassword')

cluster = Cluster(['cassandra.us-east-2.amazonaws.com'], ssl_context=ssl_context, auth_provider=auth_provider, port=9142)

session = cluster.connect()

r = session.execute('select * from system_schema.keyspaces')

print(r.current_rows)
```