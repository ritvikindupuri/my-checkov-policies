# AWS provider v4+ idiom: encryption lives in its own resource rather than in an
# inline server_side_encryption_configuration block on the bucket.
resource "aws_s3_bucket" "pass" {
  bucket = "my-encrypted-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "pass" {
  bucket = aws_s3_bucket.pass.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}
