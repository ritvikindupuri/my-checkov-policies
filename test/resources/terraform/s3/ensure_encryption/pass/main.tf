resource "aws_s3_bucket" "pass" {
  bucket = "my-encrypted-bucket"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "aws:kms"
      }
    }
  }
}
