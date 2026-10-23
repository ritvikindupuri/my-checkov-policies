# Fails: encryption_type explicitly set to AES256 (default AWS algorithm)
resource "aws_ecr_repository" "fail_aes256" {
  name = "fail-aes256"
  encryption_configuration {
    encryption_type = "AES256"
  }
}

# Fails: missing encryption_configuration block (AWS default is AES256)
resource "aws_ecr_repository" "fail_missing_encryption_config" {
  name = "fail-missing-encryption-config"
}

# Fails: empty encryption_configuration block (defaults to AES256 in AWS)
resource "aws_ecr_repository" "fail_empty_encryption_config" {
  name = "fail-empty-encryption-config"
  encryption_configuration {}
}
