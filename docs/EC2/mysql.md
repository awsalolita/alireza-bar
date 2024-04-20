

* install mysql
* then start it
* then get the temp password from log file
* change user root , localhost password 
```
sudo mysql_secure_installation

ALTER USER 'root'@'localhost' IDENTIFIED BY 'ooVsRCalC5&U1';
CREATE USER 'root'@'%' IDENTIFIED BY 'ooVsRCalC5&U1';
GRANT REPLICATION CLIENT  ON *.* TO 'root'@'%';
GRANT REPLICATION SLAVE ON *.* TO 'root'@'%';
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
```
* in /etc/my.cnf , add
```
server_id=1
log_bin = /var/log/mysql/mysql-bin.log
binlog_format=ROW
expire_logs_days=1
binlog_checksum=NONE
binlog_row_image=FULL
log_slave_updates=TRUE
```
* create bin file
```
mkdir /var/log/mysql
sudo chown -R mysql:mysql /var/log/mysql/
sudo chmod -R 755 /var/log/mysql/
```
* check with
```
SHOW VARIABLES LIKE 'log_bin';
SHOW GLOBAL VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile=ON; 
```

```
{
  "rules": [
    {
      "rule-type": "selection",
      "rule-id": "429919023",
      "rule-name": "429919023",
      "object-locator": {
        "schema-name": "sys",
        "table-name": "%"
      },
      "rule-action": "exclude",
      "filters": []
    },
    {
      "rule-type": "selection",
      "rule-id": "429917237",
      "rule-name": "429917237",
      "object-locator": {
        "schema-name": "performance_schema ",
        "table-name": "%"
      },
      "rule-action": "exclude",
      "filters": []
    },
    {
      "rule-type": "selection",
      "rule-id": "429916370",
      "rule-name": "429916370",
      "object-locator": {
        "schema-name": "mysql",
        "table-name": "%"
      },
      "rule-action": "exclude",
      "filters": []
    },
    {
      "rule-type": "selection",
      "rule-id": "429915408",
      "rule-name": "429915408",
      "object-locator": {
        "schema-name": "information_schema ",
        "table-name": "%"
      },
      "rule-action": "exclude",
      "filters": []
    },
    {
      "rule-type": "selection",
      "rule-id": "429883044",
      "rule-name": "429883044",
      "object-locator": {
        "schema-name": "awsdms_control ",
        "table-name": "%"
      },
      "rule-action": "exclude",
      "filters": []
    },
    {
      "rule-type": "selection",
      "rule-id": "429823266",
      "rule-name": "429823266",
      "object-locator": {
        "schema-name": "%",
        "table-name": "%"
      },
      "rule-action": "include",
      "filters": []
    }
  ]
}
```


# task settings 
```
{
    "Logging": {
        "EnableLogging": true,
        "EnableLogContext": true,
        "LogComponents": [
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "TRANSFORMATION"
            },
            {
                "Severity": "LOGGER_SEVERITY_ERROR",
                "Id": "SOURCE_UNLOAD"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "IO"
            },
            {
                "Severity": "LOGGER_SEVERITY_ERROR",
                "Id": "TARGET_LOAD"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "PERFORMANCE"
            },
            {
                "Severity": "LOGGER_SEVERITY_ERROR",
                "Id": "SOURCE_CAPTURE"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "SORTER"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "REST_SERVER"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "VALIDATOR_EXT"
            },
            {
                "Severity": "LOGGER_SEVERITY_ERROR",
                "Id": "TARGET_APPLY"
            },
            {
                "Severity": "LOGGER_SEVERITY_ERROR",
                "Id": "TASK_MANAGER"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "TABLES_MANAGER"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "METADATA_MANAGER"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "FILE_FACTORY"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "COMMON"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "ADDONS"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "DATA_STRUCTURE"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "COMMUNICATION"
            },
            {
                "Severity": "LOGGER_SEVERITY_DEFAULT",
                "Id": "FILE_TRANSFER"
            }
        ],
        "CloudWatchLogGroup": "dms-tasks-replmain",
        "CloudWatchLogStream": "dms-task-GRK4TF4FNREL3IMXZMOQPDQ3HI"
    },
    "StreamBufferSettings": {
        "StreamBufferCount": 3,
        "CtrlStreamBufferSizeInMB": 5,
        "StreamBufferSizeInMB": 8
    },
    "ErrorBehavior": {
        "FailOnNoTablesCaptured": true,
        "ApplyErrorUpdatePolicy": "LOG_ERROR",
        "FailOnTransactionConsistencyBreached": false,
        "RecoverableErrorThrottlingMax": 1800,
        "DataErrorEscalationPolicy": "SUSPEND_TABLE",
        "ApplyErrorEscalationCount": 0,
        "RecoverableErrorStopRetryAfterThrottlingMax": true,
        "RecoverableErrorThrottling": true,
        "ApplyErrorFailOnTruncationDdl": false,
        "DataTruncationErrorPolicy": "LOG_ERROR",
        "ApplyErrorInsertPolicy": "LOG_ERROR",
        "EventErrorPolicy": "IGNORE",
        "ApplyErrorEscalationPolicy": "LOG_ERROR",
        "RecoverableErrorCount": -1,
        "DataErrorEscalationCount": 0,
        "TableErrorEscalationPolicy": "STOP_TASK",
        "RecoverableErrorInterval": 5,
        "ApplyErrorDeletePolicy": "IGNORE_RECORD",
        "TableErrorEscalationCount": 0,
        "FullLoadIgnoreConflicts": true,
        "DataErrorPolicy": "LOG_ERROR",
        "TableErrorPolicy": "SUSPEND_TABLE"
    },
    "TTSettings": {
        "TTS3Settings": null,
        "TTRecordSettings": null,
        "EnableTT": false
    },
    "FullLoadSettings": {
        "CommitRate": 10000,
        "StopTaskCachedChangesApplied": false,
        "StopTaskCachedChangesNotApplied": false,
        "MaxFullLoadSubTasks": 8,
        "TransactionConsistencyTimeout": 600,
        "CreatePkAfterFullLoad": false,
        "TargetTablePrepMode": "DROP_AND_CREATE"
    },
    "TargetMetadata": {
        "ParallelApplyBufferSize": 0,
        "ParallelApplyQueuesPerThread": 0,
        "ParallelApplyThreads": 0,
        "TargetSchema": "",
        "InlineLobMaxSize": 0,
        "ParallelLoadQueuesPerThread": 0,
        "SupportLobs": true,
        "LobChunkSize": 0,
        "TaskRecoveryTableEnabled": false,
        "ParallelLoadThreads": 0,
        "LobMaxSize": 32,
        "BatchApplyEnabled": false,
        "FullLobMode": false,
        "LimitedSizeLobMode": true,
        "LoadMaxFileSize": 0,
        "ParallelLoadBufferSize": 0
    },
    "BeforeImageSettings": null,
    "ControlTablesSettings": {
        "historyTimeslotInMinutes": 5,
        "HistoryTimeslotInMinutes": 5,
        "StatusTableEnabled": false,
        "SuspendedTablesTableEnabled": false,
        "HistoryTableEnabled": false,
        "ControlSchema": "",
        "FullLoadExceptionTableEnabled": false
    },
   "LoopbackPreventionSettings": {
    "EnableLoopbackPrevention": true,
    "SourceSchema": "<DB>",
    "TargetSchema": "<DB>"
  },
    "CharacterSetSettings": null,
    "FailTaskWhenCleanTaskResourceFailed": false,
    "ChangeProcessingTuning": {
        "StatementCacheSize": 50,
        "CommitTimeout": 1,
        "BatchApplyPreserveTransaction": true,
        "BatchApplyTimeoutMin": 1,
        "BatchSplitSize": 0,
        "BatchApplyTimeoutMax": 30,
        "MinTransactionSize": 1000,
        "MemoryKeepTime": 60,
        "BatchApplyMemoryLimit": 500,
        "MemoryLimitTotal": 1024
    },
    "ChangeProcessingDdlHandlingPolicy": {
        "HandleSourceTableDropped": true,
        "HandleSourceTableTruncated": true,
        "HandleSourceTableAltered": true
    },
    "PostProcessingRules": null
}
```