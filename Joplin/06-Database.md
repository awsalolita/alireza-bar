# RDS
* backup
	* retention default 7
	* retention can be 1-35 days
* parameter group
	* like `max_connections` , `auto commit` 
	* apply to instances
	* static & dynamic
		* static: manual reboot
		* dynamic : without reboot
			* only cli and api
* option group
	* mysql , oracle , Microsoft , mariadb
	* extentions and modules for postgres
	* more memory maybe
	* types
		* permanent 
			* cannot be removed
		* persistent
			* dissasociate first 
* burstable , memory optimized , standard class

* AZ
	* single
	* multi AZ
		* Instance
			* primary + replica (not readable)
		* Cluster
			* primary + 2replica (readable) 
		* takes snapshot at first , so you can encounter high latency

* RDS proxy
	* prevent memory exhaustion of the db
	*  manage connections

* read replica
	* snapshot + async replication
	* auth with public key
	* guarantee more than 5 read replica
	* 15 instance for mysql maria psql + you can read replica chain
	* 5 instance for oracle , windows + you cant 
	* you can write on mysql + oracle read replicas with Parameter Group
	* if you delete manually 
		* postgres needs manual
		* 
* replication from outside
	* Binlog
	* GTID base

* backup
	* first one is a full backup , others are incremental
	* automatic
		* if u disable auto backups are deleted
	* manual
		* 2 lambda
* copies of snapshots and backup are manual
	*  snapshot cannot be encrypted by default
		*  can be with custom key


* backup
	* backup : automatic , incremental , PITR
	* snapshot : full backup , dont support PITR
* restore
	* a new rds instance is created with new endpoint
	* PITR
		* snapshot + Transaction logs
		* lazy loading
			* to prevent this , you can perform full table scan like select *
* DB Subnet Group 
	* subnet can be changed 
		* cant
			* multi az
			* read replica
			* its a read instance -> promote to be able to move
### Questions
* IAM DB authentication will allow you to authenticate to your DB instance via an authentication token. Authentication tokens expire in 15 minutes, making it suitable for temporary connections. This is available in MariaDB, MySQL, and PostgreSQL.



# Aurora
* Crash Recovery
	* partition volumes to 10gb segments
	* you donts need binary logging
* 3 AZ * 2 = 6 copies
* storage layer decoupled
*  continuous backup

* parameter group
	* instance 
	* cluster
		* cluster overwrite instance 
		* in cluster level changing the PG takes effect immediately , instance level needs reboot

* Scaling
	* Storage Scaling
		* automatic , 10 GB 
	* AutoScaling Policy
		* horizontal
	* Compute Scaling
		* vertical
		* horizontal : read rpl
		* max_connection variable + RDS proxy

* Endpoints
	* cluster (w)
	* reader (r)
	* instance (specific)
	* custom 
		* for loadbalancing (for example , low and high capacity for read replica )

* authentication
	* password
	* iam 
	* kerberos , windows AD

* multi master
	* DDL operation doesnt happen concurrently on a table
	* only mysql
	* two writer per cluster
	* no read replica 

* backtracking
	* doesnt restore to a new instance 
	* few minutes downtime
	* only mysql
	* redo and undo 
	* impact the whole db cluster
	* enabled on at new creation or creation from snapshot
	* stop application
	* you must disable cross region repl
	* cant be used with multi master 
	* up to 72 hours 

* Replication
	* cross region only for mysql 
	* update `binlog_format=MIXED`
	* from
		* Mysql RDS to aurora
			* create read replica (type = aurora)
			* once replication lag reaches zero stop write on RDS
			* promote and update endpoint
		* Mysql Cluster to aurora
			* enable binary logging on source db
			* create snapshot 
			* use snapshot to load
			* start replication on target to get data from source

* failover
	* if the master dont have read replica , aurora makes another master in the same AZ
*  Global db
	*  not auto failover
* Global db vs cross region read replica
	* global better , under 1 second , cross region takes longer and not for postgres

* modify VPC
	* clone the db in a different vpc 
		* must be in the same AZ
		* subnet should be the same AZ
		* downtime
		* create endpoint
	* take snapshot
	* setup replication (only for mysql engine)
		* manual replication with binlog

* parallel query
	* different in mysql and postgres
	* when?
		* long running queries
		* large tables
	* usable or db.r* flavour
	* enable by PG

* Aurora Clones
	* COW
	* doesnt duplicate storage
	* has to be in the same region and AZ and be in diff aws account
	* like forking a git repo

* caching 
	* apg_ccm_enabled , cluster parameter

* V1 vs V2
	* v1 ACU min can be 0
	* v2 min can be 0.5

### Question
* You don’t need binary logging for replication or PITR, and enabling binary logging increases recovery time after a crash. You only need binary logging for external replication and external binary log streams. 


# DynamoDB

* partitions
	* upto 10 gb
	* hash function on partition key to see which partition
	* R/W UC

* indexes
	* global
		* sort and partition key 
	* local
		* only different sort key
		* free to create
		* 5 per table
		* 
* 2 R and W Capacity Unit per transaction 
* 1 RCU 
* burst Capacity
* backup
	* PITR needs to be enabled
	* on demand snapshot

* restore
	* PITR setting + scaling policy and cloud watch metrics need to be configured manually

* network
	* vpc endpoint
		* interface 
		* gateway

* Streams
	* records of insert delete ... (WAL?)
	* 24h even when deleted
	* what is captured
		* Keys only
			* key attributes
		* New image
			* key attributes and values new
		* Old image
			* key attributes and values old

* DAX
	* 3 Nodes at least 
	* cache hit
	* DAX Client
	* sits between dynamo and application
	* eviction policy
	* scaling
		* support to 10 read replica
	* specific table or all 


# RedShift
* leader and compute nodes
* scale
	* classic resize
		* copy table and metadata 
		* source node goes to read only mode
	* elastic resize	
		* in place resize 
		* cant downgrade
		* faster
* unique keys doesnt matter 
* database data to s3 and then copy to redshift(COPY)
* copy data directly from databases (UNLOAD)
### Questions
* cant delete redshift automated snapshots
* Neptune is a serverless fully managed graph database.

Amazon Neptune is designed to efficiently store, query, and analyze highly connected datasets, such as social networks, recommendation engines, knowledge graphs, fraud detection, and other graph-based use cases.

Neptune excels in handling scenarios where the relationships between entities and their connections are critical.

However, Neptune **is not** primarily designed to handle traditional relational database use cases. While it does offer some relational-like features, Neptune's primary focus is on graph-based data.

Relational data with complex join operations are better served with traditional relational databases, such as Amazon RDS or Amazon Aurora.

* **Which scaling option will automatically scale your Redshift cluster by adding Redshift clusters to support concurrent users and queries?**
**Concurrency scaling** is a Redshift feature that is mainly designed to support concurrent demand. It distributes the workload by automatically adding more compute power temporarily to serve sudden spikes in concurrent users and query activity.

* DocumentDB can have upto 15 read replica for better read performance
* What distinguishes the RA3 Redshift node from other nodes?
The Dense Compute (DC) node is meant for compute-intensive workloads. While the RA3 node can handle large data warehouses,

If the data in an RA3 node grows beyond the size of the local SSDs, Amazon Redshift managed storage automatically offloads that data to Amazon S3.
RA3 provides **separation** of compute (number of nodes) and storage (amount of local SSD storage)

* QLDB for immutable records
* Redshift Spectrum? run complex SQL queries directly on data stored in Amazon S3, without the need to load or transform the data into the Redshift cluster
* MMP , It enables **parallel** processing of queries across multiple compute nodes in a Redshift cluster.

# In-Memory DB
* backup
	* cannot backup individual node
	* increase reserved-memory-percent
* scaling
	* memcache
		* vertical
			* new cluster
		* horizontal
			* ez , only adding endpoints
			* 40 nodes per cluster
	* Redis
		* vertical
			* single instance -> new instance
		* horizontal
### Question
* **The Memcached engine doesn’t support cluster mode**.
* memcache doesnt have backup feature
* Cluster mode enabled has Multi-AZ enabled by default, and you can’t disable auto-failover with this configuration.
* Cluster mode disabled has the auto-failover feature enabled by default. You can opt out of the auto-failover feature if cluster mode is disabled.
* Enabling cluster-mode doesn’t guarantee having a Multi-AZ deployment. 

# DMS and SCT
* replication instance do dms job
* migration types
	* full load
		* initial migration
		* can result in downtime
	* cdc
		* minimal downtime
		* syncing the target

* redis to elasticache
	* req
		* target needs to have
			* multi az enable
			* no encryption
			* dont have global datastore
		* source
			* AUTH disabled
* SCT
	* extraction agent
		* different source and target
	* replication agent
		* gigantic size
	*  
## Questions
* in SCT extraction agent doesnt convert
* "Full LOB mode" means that large object data types typically such as images, audio, video, or even just long text fields are all migrated regardless of how big they are. This option can slow down the migration. “Limited LOB mode” means that you’re placing a restriction on the migration of LOB data based on size.


* rds read and source replicas can have different schemas 
* rds can have replication delay


# CF for DB
* noEcho parameter for passwords
* mappings
	* dynamic
* detect drifts with cli and aws config
* TerminationProtection and DeletionPolicy
	* termination prevents everything created in CF
	* Deletion Policy to retain
## Questions
* DeletePolicy protects RDS instances from accidental deletions even when the stack is deleted.
* DeletionProtection allows you to lock your database and prevent it from being deleted.
* CloudWatch Contributor Insights for DynamoDB allows you to analyze and visualize query patterns, helping you identify high-contributing items and understand which attributes are causing high usage. This feature assists in performance monitoring, optimization, and troubleshooting by providing insights into the most impactful queries and their contributors

# security
* Iam db authentication
	* mysql , mariadb , postgres , documentdb , neptune , 
	* steps
		* enable iam db authentication
		* create db users 
			* in mysql `CREATE USER Ali IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS'`
			* in postgres `CREATE USER ALI ; GRANT rds_iam to ALI;`
* iam for dynamodb
	* 