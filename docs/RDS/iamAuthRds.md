# iam authentication

* create iam role that has a policy for rds iam 
* enable ssl for a user 
```
mysql -h <> -P 3306 -u admin -p
ALTER USER 'admin'@'%' REQUIRE SSL;
```
* download certificate bundle
```
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```
* connect using ssl
```
mysql -h <> --ssl-ca=global-bundle.pem --ssl-mode=REQUIRED -P 3306 -u admin -p
```

* create user for iam
```
CREATE USER jane_doe IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS'; 
ALTER USER 'jane_doe'@'%' REQUIRE SSL;     
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'new_admin_user'@'%' WITH GRANT OPTION;
```

* iam connection
```
RDSHOST=""
TOKEN="$(aws rds generate-db-auth-token --hostname $RDSHOST --port 3306 --username jane_doe)"
mysql --host=$RDSHOST --port=3306 --ssl-ca=global-bundle.pem --enable-cleartext-plugin --user=jane_doe --password=$TOKEN
```