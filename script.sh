#!/bin/sh
aws appconfig get-configuration --application app1 --environment env1 --configuration appconf1 --client-id app1 server.ini --region us-east-1
