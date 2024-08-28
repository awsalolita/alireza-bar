# Setup

* Create Security configuration for client side encryption or serverside for s3
```bash
hadoop fs -put outputFile.txt s3://BUCKET/
hadoop fs -cat s3://BUCKET/outputFile.txt
hadoop fs -get s3://BUCKET/outputFile.txt ./localfile
```