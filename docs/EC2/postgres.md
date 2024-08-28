
* for replication 
* DBClusterParameterGroup
```
rds.logical_replication: 1
wal_sender_timeout: 0
```

```bash
yum install -y postgresql15-test-rpm-macros.noarch
# password prompt by default
psql -h database-1.cluster-c7c2o0kgmpvz.us-east-1.rds.amazonaws.com -U postgres 
psql -h database-1.cluster-c7c2o0kgmpvz.us-east-1.rds.amazonaws.com -U pirate -d postgres
# import sql file
psql -h database-1.cluster-c7c2o0kgmpvz.us-east-1.rds.amazonaws.com -U postgres  < database.sql 
```
# user with priviledge
```sql
CREATE ROLE pirate LOGIN PASSWORD 'asjar+_)(0012';

GRANT ALL ON <table> TO pirate;
GRANT ALL PRIVILEGES ON DATABASE "MYDB" to pirate;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pirate;
```
* show db
```sql
\l
\c databasename
# show tables 
\dt
# detail about table
\d table_name
```
* show 
