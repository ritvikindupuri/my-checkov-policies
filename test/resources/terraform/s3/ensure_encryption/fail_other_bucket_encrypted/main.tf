# An encryption resource exists in the same module, but it targets a different
# bucket — aws_s3_bucket.unencrypted must still fail.
resource "aws_s3_bucket" "encrypted" {
  bucket = "my-encrypted-bucket"
}

resource "aws_s3_bucket" "unencrypted" {
  bucket = "my-unencrypted-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encrypted" {
  bucket = aws_s3_bucket.encrypted.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
