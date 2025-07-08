resource "random_id" "dynamodb_suffix" {
  byte_length = 4
}

resource "aws_dynamodb_table" "contact_form" {
  name           = "${var.table_name}_${random_id.dynamodb_suffix.hex}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }
}
