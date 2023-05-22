import json
import boto3
import os
import boto3
from datetime import datetime

client = boto3.client('logs')
group_name = os.environ["LOG_GROUP_NAME"]
stream_name = os.environ["LOG_STREAM_NAME"]


def lambda_handler(event, context):
    client.put_log_events(
        logGroupName=group_name,
        logStreamName=stream_name,
        logEvents=[
            {
                'timestamp': int(datetime.now().timestamp() * 1000),
                'message': f"Event We've been invoked"
            }
        ]
    )

    return {
        "isBase64Encoded": False,
        "statusCode": "200",
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "id": 'root',
            "name": 'Parent',
            "children": [
                {
                    "id": '1',
                    "name": 'Child - 1',
                },
                {
                    "id": '3',
                    "name": 'Child - 3',
                    "children": [
                        {
                            "id": '4',
                            "name": 'Child - 4',
                        },
                    ],
                },
            ],
        })
    }
