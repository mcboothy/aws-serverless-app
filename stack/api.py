import os
from constructs import Construct
from stack.util import Util
from typing import Dict
from aws_cdk import (
    aws_iam as iam,
    aws_logs as logs,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
)


class API(Construct):

    def deploy(
        self,
        log_group: logs.LogGroup,
    ) -> apigw.RestApi:
        
        log_stream = logs.LogStream(
            self, 
            Util.generate_object_name(f"api-gateway"), 
            log_group=log_group,
            log_stream_name=Util.generate_object_name("api-gateway"))    
                                       
        # deploy API Gateway
        role = Util.create_role(
            self,
            name= Util.generate_object_name("api-role"),
            principal=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ]
        )    
        
        env = {                
            "LOG_GROUP_NAME": log_group.log_group_name,
            "LOG_STREAM_NAME": log_stream.log_stream_name,
        }
        
        api = apigw.RestApi(
            self, 
            "api", 
            rest_api_name= Util.generate_object_name("api"),
        )
        endpoint1_resource = api.root.add_resource('endpoint1')
        endpoint2_resource = api.root.add_resource('endpoint2')       
        
        path = os.path.abspath(os.path.dirname(__file__) + "/../assets/lambda")               
        self.add_api_method(f"{path}/method_1", endpoint1_resource, role, env)
        self.add_api_method(f"{path}/method_2", endpoint2_resource, role, env)

        return api
    
    def add_api_method(
        self, 
        handler_path: str,
        resource: apigw.Resource,
        role: iam.Role,
        env_vars: Dict[str, str] 
    ) -> None:            
        name = resource.path[1:].replace('/', '-')            
        resource.add_method(
            "POST", 
            apigw.LambdaIntegration(
                _lambda.Function(
                    self,
                    name,
                    function_name=Util.generate_object_name(name),
                    runtime=_lambda.Runtime.PYTHON_3_9,
                    handler="index.lambda_handler",
                    role= role,
                    code=_lambda.Code.from_asset(handler_path),
                    environment=env_vars,
                ),
                passthrough_behavior= apigw.PassthroughBehavior.WHEN_NO_TEMPLATES
            )
        )    