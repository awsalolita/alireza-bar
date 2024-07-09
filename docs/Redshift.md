* copy data from s3
```
copy  feedback.product_feedback
from 's3://s3productreview-us-east-1-083190880943/083190880943-SENTIMENT-77ebee8453d77196be6436542877fa83/output/output' 
iam_role 'arn:aws:iam::083190880943:role/S3AccessRoleRedshift'
json 'auto';
```