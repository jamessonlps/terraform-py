resource "aws_instance" "this_var_instance_index" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var_instance_type
  key_name                    = "defaul-key-pair-james"
  subnet_id                   = aws_subnet.this.id
  vpc_security_group_ids      = [aws_security_group.this.id]
  associate_public_ip_address = true

  tags = {
    Name = var_tag_name
  }
}


output "instance_id_var_instance_index" {
  description = "ID of the EC2 instance"
  value       = aws_instance.this_var_instance_index.id

  depends_on = [
    aws_instance.this_var_instance_index
  ]
}

