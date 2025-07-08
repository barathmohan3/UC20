resource "aws_lambda_function" "contact_handler" {
  function_name = var.lambda_name
  role          = var.lambda_role_arn
  handler       = var.handler
  runtime       = var.runtime
  filename      = var.lambda_zip_path
  timeout       = 10
  environment {
    variables = var.env_vars
  }
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.contact_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = var.source_arn
}
