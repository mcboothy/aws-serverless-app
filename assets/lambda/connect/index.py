import json
import boto3
import os
import boto3
from datetime import datetime
 
group_name = os.environ["LOG_GROUP_NAME"]
stream_name = os.environ["LOG_STREAM_NAME"]
table_name = os.environ["TABLE_NAME"]

resource = boto3.resource('dynamodb',region_name=os.environ["AWS_REGION"])
table = resource.Table(table_name)   
client = boto3.client('logs')

def lambda_handler(event, context):
    client.put_log_events(
        logGroupName= group_name,
        logStreamName= stream_name,
        logEvents=[
            {
              'timestamp': int(datetime.now().timestamp() * 1000),
              'message': json.dumps(event, indent=4)
            }
        ]
    )
    
    table.put_item(Item={"connectionId": event["requestContext"]['connectionId']})        
            
    return {
        "isBase64Encoded": False,
        "statusCode": "200",
        "headers": {
            "Content-Type" : "application/json",
        }
    }        