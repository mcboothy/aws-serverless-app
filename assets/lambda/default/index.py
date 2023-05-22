import json
import boto3
import os
import boto3
from datetime import datetime
 
group_name = os.environ["LOG_GROUP_NAME"]
stream_name = os.environ["LOG_STREAM_NAME"]
table_name = os.environ["DB_TABLE_NAME"]

resource = boto3.resource('dynamodb',region_name=os.environ["AWS_REGION"])
table = resource.Table(table_name)   
logs_client = boto3.client('logs')
api_client = boto3.client('apigatewaymanagementapi')

def lambda_handler(event, context):
    logs_client.put_log_events(
        logGroupName= group_name,
        logStreamName= stream_name,
        logEvents=[
            {
              'timestamp': int(datetime.now().timestamp() * 1000),
              'message': json.dumps(event, indent=4)
            }
        ]
    )
    
    body = json.loads(event["body"])     
    response = table.scan(ProjectionExpression='connectionId')    
    
    for connection in response["Items"]:
        response = api_client.post_to_connection(
            Data=body,
            ConnectionId=connection
        )        
    
    return {
        "isBase64Encoded": False,
        "statusCode": "200",
        "headers": {
            "Content-Type" : "application/json",
        },        
        "body": json.dumps({"message": "Success"})
    }        