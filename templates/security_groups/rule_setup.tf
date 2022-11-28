resource "aws_security_group_rule" "var_name_rule" {
  type              = var_type
  from_port         = var_from_port
  to_port           = var_to_port
  protocol          = var_protocol
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = var_sg_id
}
