
resource "aws_iam_user" "var_iam_user_name" {
  name = "var_iam_user_name"
  path = "/terraform-user/"

  tags = {
    tag-key = "var_iam_tag"
  }
}

resource "aws_iam_access_key" "var_iam_user_name" {
  user = aws_iam_user.var_iam_user_name.name
}

resource "aws_iam_user_policy" "var_iam_user_name_ro" {
  name = "test"
  user = aws_iam_user.var_iam_user_name.name

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
}

output "aws_iam_user_id_var_iam_user_name" {
  description = "ID of the user"
  value       = aws_iam_user.var_iam_user_name.id

  depends_on = [
    aws_iam_user.var_iam_user_name
  ]
}
