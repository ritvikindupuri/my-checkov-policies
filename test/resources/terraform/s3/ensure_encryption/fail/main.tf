resource "aws_s3_bucket" "fail" {
  bucket = "my-unencrypted-bucket"
}
