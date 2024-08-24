#########################
# getDistance on AWS Lambda
import json
import boto3

def prepare_response(event, msg):
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled"
            },
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": str(msg)
            }    
        ]
    }
    return response

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    table = dynamodb.Table('Graph')
    source = event['sessionState']['intent']['slots']['source']['value']['interpretedValue']
    dest = event['sessionState']['intent']['slots']['destination']['value']['interpretedValue']
    
    try:
        response = table.get_item(
            Key={
                'source': source,
                'destination': dest
            }
        )
        
        if 'Item' in response and 'distance' in response['Item']:
            distance = int(response['Item']['distance'])
        
        return prepare_response(event, distance)
    except Exception as e:
        print("Error: ", e)
        return {
                'statusCode': 400,
                'body': json.dumps('Error getting the distance!')
        }
