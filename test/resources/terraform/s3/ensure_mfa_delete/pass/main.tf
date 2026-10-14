resource "aws_s3_bucket" "pass" {
  bucket = "my-versioned-bucket"
}

resource "aws_s3_bucket_versioning" "pass" {
  bucket = aws_s3_bucket.pass.id

  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Enabled"
  }
}
