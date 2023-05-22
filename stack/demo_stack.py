import os
from constructs import Construct
from stack.api import API
from stack.websocket_api import WebSocketApi
from stack.client import Client
from stack.distribution import Distribution
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_logs as logs,
    custom_resources,    
)

class DemoStack(Stack):

    endpoint = None

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        log_group = logs.LogGroup(
            self,
            "logs",
            log_group_name=f'{construct_id}-logs',
            retention=logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        ) 
        
        rest_api = API(self, "api").deploy(log_group)
        ws_api = WebSocketApi(self, "websockets-api").deploy(log_group)
        bucket = Client(self, 'client').deploy()
        
        Distribution(self, 'distibution').deploy(rest_api, ws_api, bucket)
        
        # api_url = f'https://{api.rest_api_id}.execute-api.{os.environ["AWS_REGION"]}.amazonaws.com/prod'
        # key = 'config.js'      
        
        # custom_resources.AwsCustomResource(
        #     self, 
        #     'website-conf', 
        #     on_create=custom_resources.AwsSdkCall(
        #         service="S3",
        #         action="putObject",
        #         parameters={
        #             "Body": f'var BASE_URL = "{api_url}";',
        #             "Bucket" : bucket.bucket_name,
        #             "Key": key
        #         },
        #         physical_resource_id=custom_resources.PhysicalResourceId.of(key)
        #     ),
        #     on_delete=custom_resources.AwsSdkCall(
        #         service="S3",
        #         action="deleteObject",
        #         parameters={
        #             "Bucket" : bucket.bucket_name,
        #             "Key": key
        #         },
        #     ),
        #     policy=custom_resources.AwsCustomResourcePolicy.from_sdk_calls(
        #         resources=[f'{bucket.bucket_arn}/{key}']
        #     )
        # )        