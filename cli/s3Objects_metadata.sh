

## manifest file for s3 batch
aws s3api list-objects --bucket arpjoker --query "Contents[].{Key: Key}" --output text | awk 'BEGIN{FS="\n"}{print "arpjoker" "," $1}' manifest2.csv


## aws cli to update metadata
a=`aws s3api list-objects --bucket arpjoker --query "Contents[*].Key" --output text`

for i in $a ; do 
    aws s3api copy-object --copy-source arpjoker/$i --key $i --bucket arpjoker --metadata new=new --metadata-directive REPLACE > /dev/null
done
