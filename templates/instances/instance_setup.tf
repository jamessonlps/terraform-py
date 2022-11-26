# https://github.com/AKSarav/Terraform-Count-ForEach/blob/main/

variable "configuration" {
  description = "The total configuration, List of Objects/Dictionary"
  default     = [{}]
}


locals {
  serverconfig = [
    for srv in var.configuration : [
      for i in range(1, srv.no_of_instances + 1) : {
        instance_name   = "${srv.application_name}-${i}"
        instance_type   = srv.instance_type
        subnet_id       = srv.subnet_id
        ami             = srv.ami
        security_groups = srv.vpc_security_group_ids
      }
    ]
  ]
}

// We need to Flatten it before using it
locals {
  instances = flatten(local.serverconfig)
}

resource "aws_instance" "web" {
  for_each = { for server in local.instances : server.instance_name => server }

  ami                    = each.value.ami
  instance_type          = each.value.instance_type
  vpc_security_group_ids = each.value.security_groups
  subnet_id              = each.value.subnet_id
  tags = {
    Name = "${each.value.instance_name}"
  }
}
output "instances" {
  value       = aws_instance.web
  description = "All Machine details"
}













# resource "aws_instance" "ec2-micro" {
#   # Creates four identical aws ec2 instances
#   count = 2

#   # All four instances will have the same ami and instance_type
#   ami                         = data.aws_ami.ubuntu.id
#   instance_type               = "t2.micro"
#   subnet_id                   = aws_subnet.this.id
#   vpc_security_group_ids      = [aws_security_group.this.id]
#   associate_public_ip_address = true

#   tags = {
#     # The count.index allows you to launch a resource 
#     # starting with the distinct index number 0 and corresponding to this instance.
#     Name = "my-machine-${count.index}"
#   }
# }

# output "instance_ids" {
#   description = "IDs of EC2 instances"
#   value       = aws_instance.ec2-micro.*.id
# }
