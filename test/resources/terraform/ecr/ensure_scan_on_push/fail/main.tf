# Fails: scan_on_push explicitly set to false
resource "aws_ecr_repository" "fail_scan_disabled" {
  name = "fail-scan-disabled"
  image_scanning_configuration {
    scan_on_push = false
  }
}

# Fails: missing image_scanning_configuration block (AWS default is disabled)
resource "aws_ecr_repository" "fail_missing_scanning_config" {
  name = "fail-missing-scanning-config"
}
