resource "aws_ses_email_identity" "notify_email" {
  email = var.email
}
