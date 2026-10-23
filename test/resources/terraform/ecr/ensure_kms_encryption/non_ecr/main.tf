resource "aws_s3_bucket" "ignored_bucket" {
  bucket = "non-ecr-scope-isolation-bucket"
}
