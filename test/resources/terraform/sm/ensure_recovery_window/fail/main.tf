resource "aws_secretsmanager_secret" "fail" {
  name                    = "my-secret"
  recovery_window_in_days = 7
}
