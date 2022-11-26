# HELP_COMMAND = "help"
# MANAGE_INSTANCES_COMMAND = "manage instances"

# CREATE_SEC_GROUP_COMMAND = "create sg"
# DELETE_SEC_GROUP_COMMAND = "delete sg"
# ADD_SEC_GROUP_TO_INSTANCE_COMMAND = "add sg"

# CREATE_IAM_USER_COMMAND = "create user"
# DELETE_IAM_USER_COMMAND = "delete user"

# BREAK_COMMAND = "game over"
# EXIT_COMMAND = "exit"

COMMANDS = {
  "help": "See all available commands",
  "manage instances": "Create a new instance in your VPC",
  "apply": "Execute terraform apply if the infra is not builded",
  "create sg": "Create a new security group",
  "delete sg": "Delete a security group",
  "add sg to instance": "Delete a security group",
  "game over": "Destroy all infra builded by terraform",
  "create user": "Create a new IAM user",
  "delete user": "Delete an IAM user",
  "exit": "Finishes the application",
  "list": "Show instances, users and security groups when it exists"
}
