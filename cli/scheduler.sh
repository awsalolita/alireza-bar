#!/bin/bash

scheduler-cli create-period \
    --name "dev-weekdays" \
    --begintime 07:00 \
    --endtime 19:00 \
    --weekdays mon-fri \
    --stack $schedulerStackName

scheduler-cli create-schedule \
    --name dev-weekdays-active \
    --periods dev-weekdays \
    --timezone America/Chicago \
    --stack $schedulerStackName \
    --enforced


aws ec2 create-tags \
    --resources $devInstanceIds \
    --tags Key=Schedule,Value=dev-weekdays-active
