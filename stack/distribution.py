import os
from constructs import Construct
from typing import Dict
from aws_cdk import (
    Fn,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    aws_apigateway as api_gateway,
    aws_apigatewayv2 as agwv2,
    CfnOutput,
    Stack
)

class Distribution(Construct):
    
    def deploy(self, api: api_gateway.RestApi, ws_api: agwv2.CfnApi, bucket: s3.Bucket):               
        access_identity = cloudfront.OriginAccessIdentity(self, 'website-identity')
        bucket.grant_read(access_identity)
        
        distribution = cloudfront.Distribution(
            self, 
            'cloudfront-distribution',
            default_root_object='index.html',
            default_behavior=cloudfront.BehaviorOptions(
                origin=cloudfront_origins.S3Origin(
                    bucket, 
                    origin_access_identity=access_identity
                )
            ),
            additional_behaviors={
                "/prod/*": cloudfront.BehaviorOptions(
                    allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                    origin=cloudfront_origins.HttpOrigin(
                        domain_name=Fn.select(2, Fn.split("/", api.url)) 
                    )
                ),
                "/wsprod/*": cloudfront.BehaviorOptions(
                    allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                    origin_request_policy=cloudfront.OriginRequestPolicy(
                        self, 
                        "webSocketPolicy", 
                        origin_request_policy_name= "webSocketPolicy",
                        comment= "A default WebSocket policy",
                        cookie_behavior= cloudfront.OriginRequestCookieBehavior.none(),
                        header_behavior= cloudfront.OriginRequestHeaderBehavior.allow_list(
                            "Sec-WebSocket-Key", 
                            "Sec-WebSocket-Version",
                            "Sec-WebSocket-Protocol", 
                            "Sec-WebSocket-Accept"
                        ),
                        query_string_behavior= cloudfront.OriginRequestQueryStringBehavior.none(),
                    ),
                    origin=cloudfront_origins.HttpOrigin(
                        domain_name=f"{ws_api.ref}.execute-api.{Stack.of(self).region}.amazonaws.com",
                    )
                )                
            }
        )
                
        cf_output = CfnOutput(self, "Distribution", value=distribution.distribution_id)            
        cf_output.override_logical_id("Distribution")
                
        cf_output = CfnOutput(self, "domainname", value=distribution.domain_name)            
        cf_output.override_logical_id("domainname")
                