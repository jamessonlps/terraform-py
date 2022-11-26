variable "sg_config" {
  description = "Security Groups options"
  default     = [{}]
}


locals {
  sg_groups = [
    for sg in var.sg_config : {
      name        = sg.name
      description = sg.description
      vpc_id      = aws_vpc.this.id
    }
  ]
}


resource "aws_security_group" "terraform-sec-groups" {
  for_each = { for sec_group in local.sg_groups : sec_group.name => sec_group }

  name        = each.value.name
  description = each.value.description
  vpc_id      = aws_vpc.this.id

  tags = {
    Name = "${each.value.name}"
  }
}

output "security_groups" {
  description = "Names of the created security groups"
  value       = aws_security_group.terraform-sec-groups
}


# resource "aws_security_group_rule" "ingress_rules_http" {
#   security_group_id = aws_security_group.var_sec_group_name.id
#   protocol          = "tcp"
#   from_port         = 80
#   to_port           = 80
#   cidr_blocks       = ["0.0.0.0/0"]
# }

# resource "aws_security_group_rule" "ingress_rules_ssh" {
#   security_group_id = aws_security_group.var_sec_group_name.id
#   protocol          = "tcp"
#   from_port         = 22
#   to_port           = 22
#   cidr_blocks       = ["0.0.0.0/0"]
# }

# resource "aws_security_group_rule" "egress_rules_internet" {
#   security_group_id = aws_security_group.var_sec_group_name.id
#   protocol          = "-1"
#   from_port         = 0
#   to_port           = 0
#   cidr_blocks       = ["0.0.0.0/0"]
# }

