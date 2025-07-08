import os
import json
import boto3
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

TABLE_NAME = os.environ['TABLE_NAME']
EMAIL_TO = os.environ['EMAIL_TO']

def lambda_handler(event, context):
    data = json.loads(event['body'])
    item = {
        'id': str(uuid4()),
        'name': data['name'],
        'email': data['email'],
        'message': data['message']
    }

    # Store to DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=item)

    # Send Email
    ses.send_email(
        Source=EMAIL_TO,
        Destination={'ToAddresses': [EMAIL_TO]},
        Message={
            'Subject': {'Data': 'New Contact Form Submission'},
            'Body': {'Text': {'Data': json.dumps(item, indent=2)}}
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Form submitted successfully!'})
    }
