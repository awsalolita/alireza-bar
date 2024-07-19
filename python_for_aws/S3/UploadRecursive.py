import boto3 

import os

s3 = boto3.client('s3')

def uploadDirectory(path,bucketname):
    for root,dirs,files in os.walk(path):
        for file in files:
            s3.upload_file(os.path.join(root,file),bucketname,file)
            
            
uploadDirectory('./s3-bucket-list-jam-logs' , 'aws-jam-arpjoker')