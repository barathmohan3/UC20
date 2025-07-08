import os
import json
import boto3
from uuid import uuid4

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

# Environment variables
TABLE_NAME = os.environ['TABLE_NAME']
EMAIL_TO = os.environ['EMAIL_TO']

def lambda_handler(event, context):
    cors_headers = {
        'Access-Control-Allow-Origin': 'http://application-contact-form.s3-website-us-east-1.amazonaws.com',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,POST'
    }

    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': 'CORS preflight success'})
        }

    try:
        if 'body' not in event:
            raise ValueError("Missing 'body' in event")

        data = json.loads(event['body'])
        item = {
            'id': str(uuid4()),
            'name': data.get('name'),
            'email': data.get('email'),
            'message': data.get('message')
        }

        if not all([item['name'], item['email'], item['message']]):
            raise ValueError("Missing required fields")

        # Store in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=item)
        print("Item stored in DynamoDB:", item)

        # Send email via SES
        email_body = f"""
New contact form submission:

Name: {item['name']}
Email: {item['email']}
Message: {item['message']}
"""

        response = ses.send_email(
            Source=EMAIL_TO,
            Destination={'ToAddresses': [EMAIL_TO]},
            Message={
                'Subject': {'Data': 'New Contact Form Submission'},
                'Body': {'Text': {'Data': email_body}}
            }
        )
        print("SES response:", response)

        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': 'Form submitted successfully!'})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': str(e)})
        }
