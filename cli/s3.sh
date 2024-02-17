# enable logging
aws s3api put-bucket-logging --bucket BUCKET_NAME --bucket-logging-status file://logging.json

aws s3api get-bucket-acl --bucket BUCKET_NAME

### get public object via acl

#!/bin/bash

# List all buckets
buckets=$(aws s3api list-buckets --query "Buckets[].Name" --output text)

for bucket in $buckets; do
    echo "Checking bucket: $bucket"
    # List objects in the bucket
    objects=$(aws s3api list-objects --bucket "$bucket" --query "Contents[].Key" --output text)
    
    for object in $objects; do
        # Check each object's ACL
        acl=$(aws s3api get-object-acl --bucket "$bucket" --key "$object" --output json)
        # Check if the ACL contains public access
        if echo "$acl" | grep -q "AllUsers"; then
            echo "Public object found: s3://$bucket/$object"
        fi
    done
done

