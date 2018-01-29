import json
import os

import boto3

KEY_TABLE_NAME = os.environ['KEY_TABLE']
CLIENT = boto3.client('dynamodb')
REGION = os.environ.get('AWS_REGION')


def main(event, context):
    body = json.loads(event.get('body'))
    key = event.get('pathParameters').get('key')
    value = body.get('value')

    if not value:
        response = {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing a value for 'value' in JSON body."})
        }
        return response

    try:
        CLIENT.put_item(
            TableName=KEY_TABLE_NAME,
            Item={
                'key': {'S': key},
                'value': {'S': value},
                'region': {'S': REGION}
            }
        )
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'key': key,
                'value': value,
                'region': REGION
            }),
            "headers": {
                "Access-Control-Allow-Origin" : "*",
            },
        }
    except Exception as e:
        print(e)
        response = {
            "statusCode": 400,
            "body": json.dumps({"error": "Sorry, an error occurred while writing your key."}),
            "headers": {
                "Access-Control-Allow-Origin" : "*",
            },
        }

    return response
