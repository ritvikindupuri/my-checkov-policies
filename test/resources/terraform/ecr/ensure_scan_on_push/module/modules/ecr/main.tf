resource "aws_ecr_repository" "module_repo" {
  name = "module-repo"
  image_scanning_configuration {
    scan_on_push = true
  }
}
