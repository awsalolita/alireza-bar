# types of EC2

1.  **on demand**: pay as u go , no long term commitment , when u want to run something 24/7 this is not a good option

2. **reserved** (RI) : you have a 1 year or 3 year commitment 1) all upfront 2) partial upfront 3) no upfront

discounts : 
1 > 2 > 3 > on demand

* **diff between no upfront and on demand**: 
when u stop on demand u wont pay anymore , but with RI u are still paying cause of the yearly commitment

3. **spot instances** : the unused ec2 capacity of aws , which are available up to 90% OFF . u set a limit on the pricing for hour and it is compared to aws determined spot prices , if the amount that u set is higher , you will recieve an instance 

u get a 2 min warning before instance interruption cause of no capacity or higher prices 

so **fault tolerant app** should be considered for spot instances
These include big data, containerized workloads, continuous integration/continuous delivery (CI/CD), web servers, high-performance computing (HPC), image and media rendering, or other test and development workloads.

price table updates every 5 min

# storage
* instance storage -> deleted when instance get stopped or deleted 
* EBS