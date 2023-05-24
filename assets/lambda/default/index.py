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
logs_client = boto3.client('logs')

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
    data = json.loads(body["data"])  
    
    stage = event['requestContext']['stage']
    api_id = event['requestContext']['apiId']
    region = os.environ["AWS_REGION"]
    endpoint = f'https://{api_id}.execute-api.{region}.amazonaws.com/{stage}'
    api_client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint)

    for item in table.scan(ProjectionExpression='connectionId')["Items"]:
        api_client.post_to_connection(
            Data=json.dumps({
                'type': 'message', 
                'user': data["user"],
                'message': data["message"]
            }),
            ConnectionId=item['connectionId']
        )        
    
    return {
        "isBase64Encoded": False,
        "statusCode": "200",
        "headers": {
            "Content-Type" : "application/json",
        }
    }        