# force_destroy is optional and defaults to false, so both omitting it and setting it
# explicitly to false are compliant.
resource "aws_s3_bucket" "omitted" {
  bucket = "my-protected-bucket"
}

resource "aws_s3_bucket" "explicitly_false" {
  bucket        = "my-other-protected-bucket"
  force_destroy = false
}
