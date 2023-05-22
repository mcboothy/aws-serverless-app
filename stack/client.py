import os
from constructs import Construct
from stack.util import Util
from typing import Dict
from aws_cdk import (
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    aws_apigateway as api_gateway,
    CfnOutput
)

class Client(Construct):
    
    def deploy(self):        
        path = os.path.abspath(os.path.dirname(__file__) + "/../assets/client")   
        
        # run npm build
        if self.node.try_get_context("deploy") == "True":
            Util.run_command('npm run build', path)
        
        target_bucket = s3.Bucket(
            self, 
            "website", 
            bucket_name=Util.generate_object_name('website'),
            removal_policy= RemovalPolicy.DESTROY,        
            access_control=s3.BucketAccessControl.PRIVATE,
            auto_delete_objects=True
        )
        
        s3_deployment.BucketDeployment(
            self, 
            "website_deployment", 
            sources= [s3_deployment.Source.asset(f"{path}/build")],
            destination_bucket= target_bucket
        )

                
        return target_bucket