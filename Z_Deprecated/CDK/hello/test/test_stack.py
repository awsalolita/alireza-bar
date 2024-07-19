from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_s3 as s3 ,
    RemovalPolicy
)


class TestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # queue = sqs.Queue(
        #     self, "TestQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "TestTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))
        s3.Bucket(self , "arpjoker" ,
            block_public_access=s3.BlockPublicAccess(ignore_public_acls=False , block_public_acls = False , block_public_policy = False , restrict_public_buckets= False),
            access_control=s3.BucketAccessControl.PUBLIC_READ,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=False,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY
        )
        s3.BucketAccessControl.PUBLIC_READ