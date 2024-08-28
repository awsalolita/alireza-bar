*  a block-level storage device that you can attach to an Amazon EC2 instance
*  You can detach an EBS volume from one EC2 instance and attach it to another EC2 instance in the same **Availability Zone**

# Amazon EBS Use Cases

	* Operating systems: Boot/root volumes to store an operating system.
	* Databases

# EBS types

**IOPS SSD** : high performance , low latency , i/o intensive for nosql and rdb

**purpose**: general use for balance of money and performance , used for boot volumes , low latency , dev and test 

**optimized hdd** : hdd designed for frequently accessed, used for big data and log proccessing 

**cold hdd** : Colder data requiring fewer scans per day


# benefits 
* When you create an EBS volume, it is automatically replicated within its Availability Zone to prevent data loss

* Data encryption: All EBS volumes support encryption.

* Flexibility: EBS volumes support on-the-fly changes
* Backups: Amazon EBS provides you the ability to create backups of any EBS volume.

