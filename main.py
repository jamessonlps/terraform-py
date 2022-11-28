import os
import time
from src.commands import COMMANDS
from src.constants import *
from src.utils import *


class TerraformPy():

  def __init__(self) -> None:
    print(BLUE + BOLD + "\nStarting application...")
    os.system("terraform init")

    self.default_sec_group_id = None
    self.default_ami_id       = None
    self.default_subnet_id    = None



  def init_vpc(self):
    content = read_tfstate()
    resources = content["resources"]
    for resource in resources:
      if resource["type"] == "aws_vpc":
        return
    os.system("terraform apply -auto-approve")
    self.init_instances()
    self.init_security_groups()
    self.init_users()



  def init_instances(self):
    if (os.path.exists(FILE_INSTANCES) == False):
      # Load data
      content = read_tfstate()

      for resource in content["resources"]:
        if resource["type"] == "aws_ami":
          self.default_ami_id = resource["instances"][0]["attributes"]["id"]
        elif resource["type"] == "aws_security_group":
          self.default_sec_group_id = resource["instances"][0]["attributes"]["id"]
        elif resource["type"] == "aws_subnet":
          self.default_subnet_id = resource["instances"][0]["attributes"]["id"]

      with open(file="./templates/instances/instance_setup.tf", mode="r", encoding="utf-8") as template:
        with open(file=FILE_INSTANCES, mode="w+", encoding="utf-8") as file:
          content = template.read()
          file.write(content)

      with open(file="./templates/config/vars.json", mode="r", encoding="utf-8") as template:
        with open(file=FILE_TFVARS_JSON, mode="w+", encoding="utf-8") as config:
          content = template.read()
          content = content.replace("var_ami_id", self.default_ami_id)
          content = content.replace("var_aws_subnet_id", self.default_subnet_id)
          content = content.replace("var_aws_security_group_id", self.default_sec_group_id)
          config.write(content)
      
      print(BLUE + "\nInitializing instances configuration...")
      terraform_apply()
    


  def init_security_groups(self):
    if (os.path.exists(FILE_SECURITY_GROUPS) == False):
      with open(file="./templates/security_groups/security_group_setup.tf", mode="r", encoding="utf-8") as template:
        with open(file=FILE_SECURITY_GROUPS, mode="w+", encoding="utf-8") as file:
          content = template.read()
          file.write(content)
      print(BLUE + "\nInitializing security groups configuration...")
      terraform_apply()



  def init_users(self):
    if (os.path.exists(FILE_USERS) == False):
      with open(file="./templates/users/users_setup.tf", mode="r", encoding="utf-8") as template:
        with open(file=FILE_USERS, mode="w+", encoding="utf-8") as file:
          content = template.read()
          file.write(content)
      print(BLUE + "\nInitializing users configuration...")
      terraform_apply()



  def create_sg_group(self):
    self.init_security_groups()
    
    # Open config file and get data
    content = read_vars()
    
    name = input(BOLD + "\nEnter a name to the security group: ")
    description = input(BOLD + "Enter a description to the security group: ")

    # Check if the new security group name exists
    current_config = content["sg_config"]
    for sg in current_config:
      if sg["name"] == name:
        print(RED + "\nName for security group already exists!")
        return

    content["sg_config"].append({
      "name": name,
      "description": description
    })

    write_vars(content=content)
    terraform_apply()
  



  def create_user(self):
    self.init_users()
     # Open config file and get data
    content = read_vars()
    
    name = input(BOLD + "\nEnter a name to the user: ")
    # Check if the new user name exists
    current_config = content["users_config"]
    for user in current_config:
      if user["name"] == name:
        print(RED + "\nName for user already exists!")
        return

    content["users_config"].append({
      "name": name
    })

    write_vars(content=content)
    terraform_apply()
  


  def delete_user(self):
    username = input(BOLD + "\nEnter the user name you want to delete: ")
    content = read_vars()
      
    # Remove user from the users
    users_list = []
    for user in content["users_config"]:
      if (user["name"] != username):
        users_list.append(user)
    content["users_config"] = users_list
    
    # Update config file and apply changes
    write_vars(content=content)
    terraform_apply()
    return




  def execute(self, command: str):
    if (command in COMMANDS.keys()):
      if command == "help":
        self.help_command()
      elif command == "manage instances":
        self.manage_instances()
      elif command == "apply":
        self.init_vpc()
      elif command == "create sg":
        self.create_sg_group()
      elif command == "delete sg":
        self.delete_security_group()
      elif command == "add sg to instance":
        self.set_sg_to_instance()
      elif command == "create user":
        self.create_user()
      elif command == "delete user":
        self.delete_user()
      elif command == "list":
        self.list_resources()
      elif command == "create rule":
        self.create_rule_to_sg()
      elif command == "delete rule":
        self.delete_rule_to_sg()
      elif command == "game over":
        self.destroy()
    else:
      print(RED + BOLD + "\nInvalid command\n")



  def manage_instances(self):
    instance_type = input(BOLD + "\nEnter a type of the instances: ")
    instance_amount = input(BOLD + "Enter the number of the instances: ")

    content = read_vars()

    for instance in content["configuration"]:
      if instance["instance_type"] == instance_type:
        instance["no_of_instances"] = instance_amount

    write_vars(content=content)
    terraform_apply()



  def set_sg_to_instance(self):
    instance_name = input(BOLD + "\nEnter the instance application name: ")
    sg_name       = input(BOLD + "Enter the security group name: ")

    sg_id = self.get_sg_id_by_name(sg_name)

    if sg_id is not None:
      content = read_vars()
      # Appends the security group id in the instance configuration
      for instance in content["configuration"]:
        if (instance["application_name"] == instance_name) and (sg_id not in instance["vpc_security_group_ids"]):
          instance["vpc_security_group_ids"].append(sg_id)
          
          write_vars(content=content)
          terraform_apply()

          return
      print(RED + "\nInstance not found")
    else:
      print(RED + "\nSecurity group not found!")
    


  def delete_security_group(self):
    sg_name = input(BOLD + "\nEnter the security group name: ")

    sg_id = self.get_sg_id_by_name(sg_name)

    if sg_id is not None:
      # Remove sg id from the instances
      content = read_vars()
      for instance in content["configuration"]:
        if (sg_id in instance["vpc_security_group_ids"]):
          instance["vpc_security_group_ids"].remove(sg_id)
      
      # Remove sg from the security groups
      sg_list = []
      for sg in content["sg_config"]:
        if (sg["name"] != sg_name):
          sg_list.append(sg)
      content["sg_config"] = sg_list
      
      # Update config file and apply changes
      write_vars(content=content)
      terraform_apply()
      return
    print(RED + "\nSecurity group not found")



  def create_rule_to_sg(self):
    types = ["ingress", "egress"]
    protocols = ["tcp", "udp"]

    name      = input(BOLD + "\nEnter a name to this rule (must be unique): ")
    type_rule = input(BOLD + "Enter the type of the rule: \"ingress\" or \"egress\": ")
    from_port = input(BOLD + "Start port: ")
    to_port   = input(BOLD + "End port: ")
    protocol  = input(BOLD + "Enter the protocol: \"tcp\", \"udp\" | \"-1\" for egress: ")
    sg_name   = input(BOLD + "Enter the security group name: ")

    if (type_rule == "egress"):
      protocol = "-1"

    # Check some errors
    if type_rule not in types:
      print(RED + "\nInvalid type")
      return
    if protocol not in protocols:
      print(RED + "\nInvalid protocol")
      return
    try:
      port_in = int(from_port)
      port_out = int(to_port)
      if (port_in < 0) or (port_out < 0):
        print(RED + "\nInvalid port")
    except:
        print(RED + "\nInvalid port")

    sg_id = self.get_sg_id_by_name(sg_name)

    if sg_id is not None:
      with open("./templates/security_groups/rule_setup.tf", mode="r", encoding="UTF-8") as template_file:
        template = template_file.read()
      
      template = template.replace("var_name_rule", name)
      template = template.replace("var_type", f'"{type_rule}"')
      template = template.replace("var_from_port", from_port)
      template = template.replace("var_to_port", to_port)
      template = template.replace("var_protocol", f'"{protocol}"')
      template = template.replace("var_sg_id", f'"{sg_id}"')

      with open("./rules.tf", mode="r", encoding="UTF-8") as prev_rules:
        prev_content = prev_rules.read()

      new_content = prev_content + "\n" + template

      with open("./rules.tf", mode="w+", encoding="UTF-8") as rules_file:
        rules_file.write(new_content)

      terraform_apply()
    else:
      print(RED + "\nSecurity group not found!")



  def delete_rule_to_sg(self):
    name = input(BOLD + "\nEnter the rule name you want to delete: ")

    with open("./rules.tf", mode="r", encoding="UTF-8") as file:
      lines = file.readlines()
    
    index = 0
    list_index = []
    append = False
    # Check the lines with the rule to delete
    for l in lines:
      if f"resource \"aws_security_group_rule\" \"{name}\"" in l:
        append = True
      if append:
        list_index.append(index)
      if ("}" in l) and (append == True):
        list_index.append(index)
        append = False
        break
      index += 1

    # Copy lines that is not in the rule deleted
    content = []
    idx = 0
    for l in lines:
      if (idx not in list_index):
        content.append(l)
      idx += 1

    # rule not found
    if (len(content) == len(list_index)):
      print(RED + "\nRule not found")
      return
    
    with open("./rules.tf", "w+", encoding="UTF-8") as file:
      file.writelines(content)
    terraform_apply()



  def list_resources(self):
    os.system("terraform output")



  def help_command(self):
    print(GREEN + '\n---------------------------------------')
    print(GREEN + "You are able to execute these commands:\n" + RESET)
    for command, action in COMMANDS.items():
      print(CYAN + f"{command} - {action}" + RESET)



  def get_sg_id_by_name(self, name: str):
    content = read_tfstate()

    resources = content["resources"]
    for resource in resources:
      if (resource["type"] == "aws_security_group") and (resource["name"] == "terraform-sec-groups"):
        sg_instances = resource["instances"]
        for sg in sg_instances:
          if sg["index_key"] == name:
            return sg["attributes"]["id"]

    return None

  
  def destroy(self):
    print(RED + BOLD + "\nDestroying the world...\n")
    terraform_destroy()
    os.remove(FILE_TFVARS_JSON)
    os.remove(FILE_INSTANCES)
    try:
      os.remove(FILE_SECURITY_GROUPS)
    except FileNotFoundError:
      pass
    try:
      os.remove(FILE_USERS)
    except FileNotFoundError:
      pass


terraform_app = TerraformPy()
terraform_app.init_vpc()

if (os.path.exists(FILE_TFVARS_JSON) == False) and (os.path.exists(FILE_INSTANCES) == False):
  terraform_app.init_instances()

while True:
  try:
    command = input("\nIf you don't know the available commands, try help\n$ ")
    terraform_app.execute(command)
    if command == "game over":
      break
  except KeyboardInterrupt:
    print(RED + "\nStopping application...")
    time.sleep(1)
    break
