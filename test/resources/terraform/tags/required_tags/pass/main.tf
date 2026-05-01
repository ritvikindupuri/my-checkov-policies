resource "aws_s3_bucket" "compliant" {
  bucket = "my-compliant-bucket"

  tags = {
    Owner = "platform-team"
  }
}

resource "aws_instance" "compliant" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Owner = "platform-team"
  }
}
