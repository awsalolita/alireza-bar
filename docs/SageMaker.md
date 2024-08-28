# Prepare Dataset
## Wrangler
* Multiple sources
* data manuplation , drop column , skip missing row , split data and ...
or
## EMR
* connect to instances
```
%load_ext sagemaker_studio_analytics_extension.magics
%sm_analytics emr connect --verify-certificate False --cluster-id j-29LMN0E5HHSKX --auth-type None --language python  
```
* Query dataset
```
sqlContext = HiveContext(sqlContext)

dbs = sqlContext.sql("show databases")
dbs.show()

tables = sqlContext.sql("show tables")
tables.show()
```
* Query and load data
```
adult_df = sqlContext.sql("select * from adult_data").cache()
adult_df.limit(5).toPandas()
```


# Train
* Data Wrangler to s3 (datasets)
* in sagemaker studio , ipynb files 
* train , built in
* estimator -> image , role, bucket
```python
xgb_model = sagemaker.estimator.Estimator(
    image_uri = container,
    role = role, 
    `instance_count` = 1, 
    instance_type ='ml.m5.xlarge',
    output_path = output_path,
    sagemaker_session = sagemaker_session,
    rules=[
        Rule.sagemaker(rule_configs.create_xgboost_report())
    ]
)
```
* hyperParameters , training parameters
```python
xgb_model.set_hyperparameters(
    max_depth = 5,
    eta = 0.2,
    gamma = 4,
    min_child_weight = 6,
    subsample = 0.7,
    verbosity = 0,
    objective = 'binary:logistic',
    num_round = 800
)
```
* deploy
```python
xgb_predictor = xgb.deploy(
    initial_instance_count=1, instance_type="ml.m4.xlarge", serializer=CSVSerializer()
)
```
### run shell commands
* add !
```bash
!mkdir data
```
### Sentiment job with MXNet, 
```python
from sagemaker import get_execution_role
from sagemaker.mxnet import MXNet
m = MXNet(
    "sentiment.py",
    role=get_execution_role(),
    instance_count=1,
    instance_type="ml.m4.xlarge",
    framework_version="1.8.0",
    py_version="py37",
    distribution={"parameter_server": {"enabled": True}},
    hyperparameters={
        "batch-size": 8,
        "epochs": 2,
        "learning-rate": 0.01,
        "embedding-size": 50,
        "log-interval": 1000,
    },
)
predictor = m.deploy(initial_instance_count=1, instance_type="ml.m4.xlarge")
data = [
    "this movie was extremely good .",
    "the plot was very boring .",
    "this film is so slick , superficial and trend-hoppy .",
    "i just could not watch it till the end .",
    "the movie was so enthralling !",
]
response = predictor.predict(data)
print(response)
```

### Invoking an endpoint
```python
import io
import boto3
import csv
test_file = io.StringIO('["The movie was horrible","This should be awarded an Oscar","I did not like the ending"]')
client = boto3.client('sagemaker-runtime')
payload = test_file.getvalue()
response = client.invoke_endpoint(
  EndpointName=ENDPOINT_NAME,
  ContentType='text/csv',
  Body=payload,
  Accept='Accept'
  )
prediction = response['Body'].read().decode('utf-8')
```