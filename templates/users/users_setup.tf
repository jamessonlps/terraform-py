
variable "users_config" {
  description = "Users"
  default     = [{}]
}


locals {
  users_list = [
    for user in var.users_config : {
      name = user.name
    }
  ]
}


resource "aws_iam_user" "iam_user" {
  for_each = { for user in local.users_list : user.name => user }

  name = each.value.name
  path = "/terraform-user/"

  tags = {
    tag-key = "iam_tag"
  }
}

resource "aws_iam_access_key" "iam_user" {
  for_each = { for user in local.users_list : user.name => user }

  user = each.value.name

  depends_on = [
    aws_iam_user.iam_user
  ]
}

resource "aws_iam_user_policy" "iam_user_role" {
  for_each = { for user in local.users_list : user.name => user }

  name = "test"
  user = each.value.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:Describe*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF

  depends_on = [
    aws_iam_user.iam_user
  ]
}

output "users" {
  description = "Users"
  value       = aws_iam_user.iam_user
}
