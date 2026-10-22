variable "unresolved_scan" {
  type        = bool
  description = "Intentionally unresolved variable with no default value"
}

resource "aws_ecr_repository" "unresolved_scan_repo" {
  name = "unresolved-scan-repo"
  image_scanning_configuration {
    scan_on_push = var.unresolved_scan
  }
}
