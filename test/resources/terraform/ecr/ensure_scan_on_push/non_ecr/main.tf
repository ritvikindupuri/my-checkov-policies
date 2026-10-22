resource "aws_s3_bucket" "unrelated" {
  bucket = "non-ecr-scope-isolation-bucket"
}
