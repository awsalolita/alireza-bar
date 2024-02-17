event = {
    "source": aws.cloudwatch', 'alarmArn': 'arn:aws:cloudwatch:us-east-1: 160456506717:alarm:test alarm', 'accountId': '160456506717', 'time': '2024-02-16T10: 08: 02.566+0000', 'region': 'us-east-1', 'alarmData': {'alarmName': 'test alarm', 'state': {'value': 'ALARM', 'reason': 'Threshold Crossed: 1 out of the last 1 datapoints [
                0.19726775956284198 (16/02/24 10: 02: 00)
            ] was less than the threshold (1.0) (minimum 1 datapoint for OK -> ALARM transition).', 'reasonData': '{
                "version": "1.0",
                "queryDate": "2024-02-16T10:08:02.127+0000",
                "startDate": "2024-02-16T10:02:00.000+0000",
                "statistic": "Average",
                "period": 60,
                "recentDatapoints": [
                    0.19726775956284198
                ],
                "threshold": 1.0,
                "evaluatedDatapoints": [
                    {
                        "timestamp": "2024-02-16T10:02:00.000+0000",
                        "sampleCount": 5.0,
                        "value": 0.19726775956284198
                    }
                ]
            }', 'timestamp': '2024-02-16T10: 08: 02.566+0000'
        }, 'previousState': {'value': 'INSUFFICIENT_DATA', 'reason': 'Insufficient Data: 1 datapoint was unknown.', 'reasonData': '{
                "version": "1.0",
                "queryDate": "2024-02-16T10:04:02.129+0000",
                "statistic": "Average",
                "period": 60,
                "recentDatapoints": [],
                "threshold": 1.0,
                "evaluatedDatapoints": [
                    {
                        "timestamp": "2024-02-16T10:03:00.000+0000"
                    }
                ]
            }', 'timestamp': '2024-02-16T10: 04: 02.130+0000'
        }, 'configuration': {'metrics': [
                {'id': '24c6d8a7-4088-4ab0-d222-b01d5ed3674a', 'metricStat': {'metric': {'namespace': 'AWS/EC2', 'name': 'CPUUtilization', 'dimensions': {'InstanceId': 'i-09d24d151e73223dc'
                            }
                        }, 'period': 60, 'stat': 'Average'
                    }, 'returnData': True
                }
            ]
        }
    }
}


## be careful  , you need iam permissions for invocation
# aws lambda add-permission \
# --function-name my-function-name \
# --statement-id AlarmAction \
# --action 'lambda:InvokeFunction' \
# --principal lambda.alarms.cloudwatch.amazonaws.com \
# --source-account 111122223333 \
# --source-arn arn:aws:cloudwatch:us-east-1:111122223333:alarm:alarm-name

## parse

print(event['alarmData']['configuration'])

#give
response  = {'metrics': [
        {'id': '24c6d8a7-4088-4ab0-d222-b01d5ed3674a', 
        'metricStat': {
            'metric': {
                'namespace': 'AWS/EC2',
                 'name': 'CPUUtilization',
                  'dimensions': {
                    'InstanceId': 'i-09d24d151e73223dc'
                    }
                }, 'period': 60, 'stat': 'Average'
            }, 'returnData': True
        }
    ]
}