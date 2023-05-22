#!/usr/bin/env python3
import os
import aws_cdk as cdk
from stack.demo_stack import DemoStack

app = cdk.App()

DemoStack(
    app, 
    f'{os.getenv("STACK_NAME")}',
    env=cdk.Environment(
        account=os.getenv('AWS_ID'), 
        region=os.getenv('AWS_REGION')
    )
)

cdk.Tags.of(app).add("Team", "COEUS")

app.synth()
