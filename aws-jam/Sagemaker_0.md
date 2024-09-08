# Task 1: Only the best tricks for Mister Potato Head
### Clue 1:Autodialer (Loading the data into the dataframe)
Your first cell should load the s3 data into a dataframe. With boto3, pandas, and s3fs you can do this in one line.

Cell 1:

import boto3
import pandas as pd
import s3fs
df = pd.read_csv('s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv',low_memory=False)

### Clue 2:People sometimes make mistakes (Fixing data errors)
Exploring the data, you might see that some items are misread. In particular the formatting of this data might duplicate header information.

An easy way to see this is by looking at the "Label" column.

    df["Label"].value_counts()
You should only see two values "Benign" and "Infiltration". If you do see "Label" it means the headers were incorrectly loaded into the dataframe. This can be fixed with the following code.

df = df[df.Label != "Label"]

### Clue 3:Complete Walkthrough
Open the Amazon Sagemaker console by navigating to the Sagemaker service in the AWS Management Console
Under Notebook choose Notebook instances.
Open the instance that starts with EDA, click the “Open Jupyter” button.
You should see an empty page with Jupyter in the top right, on the right side click the “New” button and conda_python3.
Create and run the following cells in your notebook.
Cell 1:

import boto3
import pandas as pd
import s3fs
df = pd.read_csv('s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv',low_memory=False)
Cell 2:

df = df[df.Label != "Label"]
df[100:101]
You should be able to see that row 100 has a "Flow Duration" of 247

# Task 2: Shall we play a game?
### Clue 1:I always thought there was gonna be plenty of time! (Time considerations and required feature engineering)
The current data format makes it difficult to see the hours the logs were detected in. A good practice is to turn the time object into a datetime object and add an additional column for "hours".

Change Timestamp into a datetime object

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
Make a column for 'hour'

df['hour'] = df.Timestamp.dt.hour

### Clue 2:It's a boring game. It's always a tie. (Grouping relevant data to find the answer)
The CISO is wanting to know the number of Infiltration attempts each hour. One way you can sort this is by finding the number of "Infiltration" attempts for each hour.

df.groupby('hour')['Label'].value_counts()

### Clue 3:Complete Walkthrough
Open the Amazon Sagemaker console by navigating to the Sagemaker service in the AWS Management Console
Under Notebook choose Notebook instances.
Open the instance that starts with EDA, click the “Open Jupyter” button.
You should see an empty page with Jupyter in the top right, on the right side click the “New” button and conda_python3.
Create and run the following cells in your notebook.
Cell 1:

import boto3
import pandas as pd
import s3fs
df = pd.read_csv('s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv',low_memory=False)
Cell 2:

df = df[df.Label != "Label"]
df[100:101]
Cell 3:

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['hour'] = df.Timestamp.dt.hour
df.groupby('hour')['Label'].value_counts()
You should be able to see that the most Infilteration attacks happened at 11 with 33552.