import json
import os

import boto3

KEY_TABLE_NAME = os.environ['KEY_TABLE']
CLIENT = boto3.client('dynamodb')
REGION = os.environ.get('AWS_REGION')


def main(event, context):
    key = event.get('pathParameters').get('key')

    try:
        resp = CLIENT.get_item(
            TableName=KEY_TABLE_NAME,
            Key={
                'key': {'S': key},
            }
        )
        item = resp.get('Item')
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'key': item.get('key', {}).get('S'),
                'value': item.get('value', {}).get('S'),
                'writeRegion': item.get('region', {}).get('S'),
                'readRegion': REGION,
            }),
            "headers": {
                "Access-Control-Allow-Origin" : "*",
            },
        }
    except Exception as e:
        print(e)
        response = {
            "statusCode": 400,
            "body": json.dumps({"error": "Sorry, an error occurred while retrieving your key."}),
            "headers": {
                "Access-Control-Allow-Origin" : "*",
            },
        }

    return response
