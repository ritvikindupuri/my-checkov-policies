resource "aws_s3_bucket" "no_tags" {
  bucket = "my-non-compliant-bucket"
}

resource "aws_instance" "wrong_tags" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Environment = "production"
  }
}
