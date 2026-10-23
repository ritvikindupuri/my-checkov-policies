variable "encryption_type" {
  type        = string
  description = "Encryption type without default, triggering Checkov directory runner limitation"
}

resource "aws_ecr_repository" "unresolved_var_repo" {
  name = "unresolved-var-repo"
  encryption_configuration {
    encryption_type = var.encryption_type
  }
}
