import os
from constructs import Construct, DependencyGroup
from stack.util import Util
from typing import Dict
from aws_cdk import (
    aws_iam as iam,
    aws_logs as logs,
    aws_apigateway as apigw,
    aws_apigatewayv2 as apigwv2,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    Stack,
    Duration
)


class WebSocketApi(Construct):

    def deploy(
        self,
        log_group: logs.LogGroup,
    ) -> apigw.RestApi:
        
        log_stream = logs.LogStream(
            self, 
            Util.generate_object_name(f"websockets-apgw"), 
            log_group=log_group,
            log_stream_name=Util.generate_object_name("websockets-apgw"))    
                                       
        # deploy API Gateway
        role = Util.create_role(
            self,
            name= Util.generate_object_name("api-role"),
            principal=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda.amazonaws.com"),
                iam.ServicePrincipal("apigateway.amazonaws.com")),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),           
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),                   
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaRole"),     
            ],
            statements=[
                {
                    "Effect": "Allow",
                    "Action": [
                        "execute-api:*",
                        "apigateway:*"
                    ],
                    "Resource": "*"
                }
            ]
        )    
                                
        api = apigwv2.CfnApi(
            self, 
            "websockets-api", 
            name= Util.generate_object_name("websocket-api"),
            protocol_type= "WEBSOCKET",
            route_selection_expression= "$request.body.route_key"
        );                
        
        connections_table = dynamodb.Table(
            self, 
            'WSconnections',
            table_name=Util.generate_object_name("ws-connections"),
            partition_key=dynamodb.Attribute(name= 'connectionId', type= dynamodb.AttributeType.STRING),
            billing_mode= dynamodb.BillingMode.PAY_PER_REQUEST,
            stream= dynamodb.StreamViewType.NEW_IMAGE,
            removal_policy=RemovalPolicy.DESTROY,
        )

        env = {                
            "LOG_GROUP_NAME": log_group.log_group_name,
            "LOG_STREAM_NAME": log_stream.log_stream_name,
            "TABLE_NAME": connections_table.table_name,
        }        
                
        path = os.path.abspath(os.path.dirname(__file__) + "/../assets/lambda")               
        connect_route = self.add_api_method('connect', f"{path}/connect", api, role, env)
        disconnect_route = self.add_api_method('disconnect', f"{path}/disconnect", api, role, env)
        default_route = self.add_api_method('default', f"{path}/default", api, role, env)
               
        deployment = apigwv2.CfnDeployment(
            self, 
            "api-deployment", 
            api_id= api.ref
        )

        stage = apigwv2.CfnStage(
            self,
            "api-stage", 
            api_id= api.ref,
            deployment_id= deployment.ref,
            stage_name= "wsprod",
        )

        routes = DependencyGroup()
        routes.add(connect_route);
        routes.add(disconnect_route);
        routes.add(default_route);

        deployment.node.add_dependency(routes);               
                
        return api
    
    def add_api_method(
        self, 
        name: str,
        handler_path: str,
        api: apigwv2.CfnApi,
        role: iam.Role,
        env_vars: Dict[str, str] 
    ) -> None:            
        function =_lambda.Function(
            self,
            name,
            function_name=Util.generate_object_name(name),
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.lambda_handler",
            role= role,
            code=_lambda.Code.from_asset(handler_path),
            environment=env_vars,
            timeout=Duration.minutes(5)
        )        
                
        intergration = apigwv2.CfnIntegration(
            self, 
            f"{name}-intergration", 
            api_id= api.ref,
            integration_type= "AWS_PROXY",
            integration_uri= f"arn:aws:apigateway:{Stack.of(self).region}:lambda:path/2015-03-31/functions/{function.function_arn}/invocations",
            credentials_arn= role.role_arn
        )
        
        return apigwv2.CfnRoute(
            self, 
            f"{name}-route", 
            api_id= api.ref,
            route_key= f"${name}",
            authorization_type= "NONE",
            api_key_required= False,
            operation_name= name,
            target= f"integrations/{intergration.ref}"
        );                
        