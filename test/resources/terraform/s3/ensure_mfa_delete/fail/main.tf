resource "aws_s3_bucket" "fail" {
  bucket = "my-versioned-bucket"
}

resource "aws_s3_bucket_versioning" "fail" {
  bucket = aws_s3_bucket.fail.id

  versioning_configuration {
    status = "Enabled"
  }
}
