import json
import os
import subprocess
from typing import List, Dict
from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as api_gateway,
)


class Util:    
    
    @staticmethod
    def generate_object_name(name: str) -> str:
        return os.getenv('STACK_NAME').lower() + "-" + name       
        
    @staticmethod
    def run_command(command: str, cwd: str):
        with subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) as process:
            while True:
                line = process.stdout.readline()
                if process.poll() is not None:
                    break
                print(line.decode('utf8'))            
        
    @staticmethod
    def cli_command(command: str):
        stream = os.popen(command)
        cli_output = stream.read()
        return json.loads(cli_output)
            
    @staticmethod
    def get_cdk_output(id: str) -> str:      
        command = f'aws cloudformation describe-stacks \
                    --stack-name {os.getenv("STACK_NAME")} \
                    --query "Stacks[0].Outputs"'
        all_outputs = Util.cli_command(command)
        for output in all_outputs:
            if (output["OutputKey"] == id):
                return output["OutputValue"]      
        return None                  
        
    @staticmethod
    def create_lambda(
        construct: Construct, 
        handler: str, 
        name: str, 
        path: str,
        env: Dict[str,str] = None, 
        managed_policies: List = None
    ) -> _lambda.Function:
        return _lambda.Function(
            construct,
            name,
            function_name=name,
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler=handler,
            role= Util.create_role(
                construct,
                name= f"{name}-role",
                principal="lambda.amazonaws.com",
                managed_policies=managed_policies
            ),
            code=_lambda.Code.from_asset(path),
            environment=env
        )
                
    @staticmethod
    def create_role(
        construct: Construct, 
        name: str, 
        principal: str, 
        statements: List[Dict] = None, 
        managed_policies: List = None
    ) -> iam.Role:         
        role = iam.Role(
            construct, 
            f'{name}-role',
            assumed_by=iam.ServicePrincipal(principal),
        )
            
        if managed_policies:
            for managed_policy in managed_policies:
                role.add_managed_policy(managed_policy)
            
        if statements:
            policy_doc = iam.PolicyDocument.from_json({
                "Version": "2012-10-17",
                "Statement": statements
            })
            
            policy = iam.Policy(
                construct, 
                f'{name}-policy',
                policy_name=f'{name}-policy',
                document=policy_doc
            )    
            
            policy.attach_to_role(role)       
                     
        return role    

    @staticmethod
    def add_api_method(
        connstruct: Construct, 
        http_method: str,
        path: str,
        handler: str,
        handler_path: str,
        parent_resource: api_gateway.Resource,
        role: iam.Role,
        env_vars: Dict[str, str] 
    ) -> None:
        if path:
            resource = parent_resource.add_resource(path)
        else:
            resource = parent_resource
            
        name = resource.path[1:].replace('/', '-')            
        resource.add_method(
            http_method, 
            api_gateway.LambdaIntegration(
                _lambda.Function(
                    connstruct,
                    name,
                    function_name=Util.generate_object_name(name),
                    runtime=_lambda.Runtime.PYTHON_3_9,
                    handler=handler,
                    role= role,
                    code=_lambda.Code.from_asset(handler_path),
                    environment=env_vars,
                ),
                passthrough_behavior= api_gateway.PassthroughBehavior.WHEN_NO_TEMPLATES
            )
        )