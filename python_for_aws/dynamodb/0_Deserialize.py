import boto3
from boto3.dynamodb.conditions import Key, Attr
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from decimal import *

# change something like 
a = {'CustID': {'S': 'task1test1record'}, 'TnValue': {'N': '250'}}
# to 
b = {'TotalTnValue': Decimal('333'), 'CustID': '8731f0c344ce4f10'}
# use DESERIALIZER
def ddb_deserialize(r, type_deserializer = TypeDeserializer()):
    return type_deserializer.deserialize({"M": r})

def ddb_serialize(r, type_serializer = TypeSerializer()):
    return type_serializer.serialize(r)["M"]

print(ddb_serialize(b))