# python3 code
* writing 
```python
import boto3
client_tsw = boto3.client('timestream-write')
records_ts [{} , {} , {}]
client_tsw.write_records(DatabaseName=TS_DB_NAME, TableName=TS_TABLE_NAME, Records=records_ts, CommonAttributes={})
```
* querying
```python
import boto3
client_timestream = boto3.client('timestream-query')
history_duration = 600 
TRACKER_NAME = 'Device_Tracker'
TIME_DB      = 'Device_Time_DB'
TIME_TABLE   = 'Positions'
query_string = 'SELECT DeviceID, time, measure_name, measure_value::double, measure_value::bigint FROM "{}"."{}" WHERE time BETWEEN ago({}s) AND now() ORDER BY time DESC'.format(TIME_DB, TIME_TABLE, history_duration)
response = client_timestream.query(QueryString=query_string)
```

