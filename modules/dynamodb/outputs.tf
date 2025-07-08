output "dynamodb_table_arn" {
  value = aws_dynamodb_table.contact_form.arn
}
output "dynamodb_table_name" {
  value = aws_dynamodb_table.contact_form.name
}
