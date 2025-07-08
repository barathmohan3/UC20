output "source_arn" {
  value = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.contact_api.id}/${aws_api_gateway_stage.prod.stage_name}/POST/contact"
}
