* application migration
* iam user with two policies 
```
AWSApplicationMigrationAgentInstallationPolicy
AWSApplicationMigrationAgentPolicy
```

```
sudo wget -O ./aws-replication-installer-init.py https://aws-application-migration-service-us-east-1.s3.amazonaws.com/latest/linux/aws-replication-installer-init.py

sudo python3 aws-replication-installer-init.py
```

* turn off Instance type right sizing in launch settings
* Replication server to migrate and Conversion server 