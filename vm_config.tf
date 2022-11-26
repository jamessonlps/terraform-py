variable "t2_micro" {
  type = map(string)
  default = {
    type = "t2.micro"
  }
}

variable "t2_medium" {
  type = map(string)
  default = {
    type = "t2.medium"
  }
}

variable "t2_large" {
  type = map(string)
  default = {
    type = "t2.large"
  }
}



data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"] # Canonical
}
