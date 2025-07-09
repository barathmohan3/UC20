# UC20

You want to create a backend for a contact form on a website. When a user submits the form, the data is sent to an API endpoint. This endpoint triggers a Lambda function that stores the data in DynamoDB and sends a notification email.

---

Architecture Components

· AWS Lambda: Handles form submissions.

· API Gateway: Exposes a RESTful endpoint (POST /contact).

· DynamoDB: Stores contact form data.

· SES (Simple Email Service): Sends notification emails.

· Terraform: Manages infrastructure as code.

· GitHub Actions: Automates deployment on code push.

---

Terraform Setup

Terraform will define:

· Lambda function (with IAM role and permissions)

· API Gateway REST API

· DynamoDB table

· SES configuration

· Deployment package (via S3 or inline zip)

· Outputs for API endpoint
