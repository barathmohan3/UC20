provider "aws" {
  region = "us-east-1"
}

module "dynamodb" {
  source     = "./modules/dynamodb"
  table_name = "contact_form_submissions"
}

module "ses" {
  source = "./modules/ses"
  email  = "barathmohan.sivas@hcltech.com"
}

module "iam" {
  source       = "./modules/iam"
  dynamodb_arn = module.dynamodb.dynamodb_table_arn
}

resource "random_id" "lambda_suffix" {
  byte_length = 4
}

module "lambda" {
  source           = "./modules/lambda"
  lambda_name      = "contact_form_lambda_${random_id.lambda_suffix.hex}"
  lambda_role_arn  = module.iam.lambda_role_arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.10"
  lambda_zip_path  = "lambda.zip"
  env_vars = {
    TABLE_NAME = "contact_form_submissions"
    EMAIL_TO   = "barathmohan.sivas@hcltech.com"
  }
  source_arn = module.api_gateway.source_arn
}

module "api_gateway" {
  source     = "./modules/api_gateway"
  api_name   = "contact_form_api"
  lambda_uri = module.lambda.contact_handler_invoke_arn
  region     = "us-east-1"
}

output "api_url" {
  value = module.api_gateway.api_endpoint
}
