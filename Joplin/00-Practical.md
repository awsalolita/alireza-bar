# ECS
* you need task definitions , a cluster
* network modes are
	* awsvpc -> every containers gets its own ENI , this can lead to ENI limit for ec2 and ip exaustion 
	* host -> the network of the ec2 , the same port
	* bridge -> basic docker port mapping
* SSH OPTIONS
	* make user with pass
	* ssm
	* connect endpoint
	* bastion
	* direct ssh