resource "aws_s3_bucket" "fail" {
  bucket        = "my-destroyable-bucket"
  force_destroy = true
}
