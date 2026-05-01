resource "aws_secretsmanager_secret" "pass" {
  name                    = "my-secret"
  recovery_window_in_days = 30
}
