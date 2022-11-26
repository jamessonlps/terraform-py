
# VPC configuration
resource "aws_vpc" "this" {
  cidr_block           = var.vpc_configuration.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "default-vpc"
  }
}

# Internet Gateway configuration
resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "default-internet-gateway"
  }
}

# Subnet configuration
resource "aws_subnet" "this" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "172.16.10.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "default-subnet"
  }
}


resource "aws_security_group" "this" {
  name        = "allow_connection"
  description = "Allow inbound traffic (SSH and HTTP)"
  vpc_id      = aws_vpc.this.id

  ingress {
    description = "SSH"
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Full access to internet"
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "default-security-group"
  }
}


# resource "aws_network_interface" "this" {
#   subnet_id       = aws_subnet.this.id
#   private_ips     = ["172.16.10.100"]
#   security_groups = [aws_security_group.this.id]

#   tags = {
#     Name = "default-network-interface"
#   }
# }


resource "aws_route_table" "this" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = {
    Name = "default-route-table"
  }
}


resource "aws_route_table_association" "this" {
  subnet_id      = aws_subnet.this.id
  route_table_id = aws_route_table.this.id
}
