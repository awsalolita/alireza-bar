import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics

tracer = Tracer()
logger = Logger()


table_name = os.environ["TABLE_NAME"]
client = boto3.client("dynamodb")


def get_user(id):
    response = client.get_item(TableName=table_name, Key={"id": {"S": id}})
    return response["Item"]


def deserialise(item):
    d = TypeDeserializer()
    return {k: d.deserialize(v) for k, v in item.items()}

@tracer.capture_lambda_handler
def handler(event, context):
    item = get_user("jammer")
    user = deserialise(item)
    return user
