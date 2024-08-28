*  security of the cloud versus security in the cloud.
responsibility of user and aws 


* authentication comes first : are  u who u say u are?
* then authorization : can u access X 

IAM policy : 
ex:
```
{"Version": "2012-10-17",    
     "Statement": [{        
          "Effect": "Allow",        
          "Action": [            
               "iam: ChangePassword",            
               "iam: GetUser"            
               ]        
          "Resource": "arn:aws:iam::995291906442:user/new"    
     }]
}
```

