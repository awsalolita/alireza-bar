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
```
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
```
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



