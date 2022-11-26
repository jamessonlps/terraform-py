import os
import time
import json
import re
import pprint
from subprocess import run, PIPE

commands = {
  "help": "See all available commands",
  "manage instances": "Create a new instance in your VPC",
  "create sg": "Create a new security group",
  "delete sg": "Delete a security group",
  "add sg to instance": "Delete a security group",
  "game over": "Destroy all infra builded by terraform",
  "create user": "Create a new IAM user",
  "delete user": "Delete an IAM user",
  "exit": "Finishes the application"
}

class TerraformPy():

  def __init__(self) -> None:
    print("Starting application...")
    os.system("terraform init")

    self.default_sec_group_id = None
    self.default_ami_id       = None
    self.default_subnet_id    = None



  def init_vpc(self):
    with open(file="./terraform.tfstate", mode="r", encoding="utf-8") as file:
      content = json.load(file)
    resources = content["resources"]
    for resource in resources:
      if resource["type"] == "aws_vpc":
        return
    os.system("terraform apply -auto-approve")



  def init_instances(self):
    # Load data
    with open(file="./terraform.tfstate", mode="r", encoding="utf-8") as file:
      content = json.load(file)
      for resource in content["resources"]:
        if resource["type"] == "aws_ami":
          self.default_ami_id = resource["instances"][0]["attributes"]["id"]
        elif resource["type"] == "aws_security_group":
          self.default_sec_group_id = resource["instances"][0]["attributes"]["id"]
        elif resource["type"] == "aws_subnet":
          self.default_subnet_id = resource["instances"][0]["attributes"]["id"]

    with open(file="./templates/instances/instance_setup.tf", mode="r", encoding="utf-8") as template:
      with open(file="instances.tf", mode="w+", encoding="utf-8") as file:
        content = template.read()
        file.write(content)

    with open(file="./templates/config/vars.json", mode="r", encoding="utf-8") as template:
      with open(file="vars.tfvars.json", mode="w+", encoding="utf-8") as config:
        content = template.read()
        content = content.replace("var_ami_id", self.default_ami_id)
        content = content.replace("var_aws_subnet_id", self.default_subnet_id)
        content = content.replace("var_aws_security_group_id", self.default_sec_group_id)
        config.write(content)
    os.system('terraform apply -auto-approve -var-file="vars.tfvars.json"')
    


  def init_sg_groups(self):
    if (os.path.exists("security_groups.tf") == False):
      with open(file="./templates/security_groups/security_group_setup.tf", mode="r", encoding="utf-8") as template:
        with open(file="security_groups.tf", mode="w+", encoding="utf-8") as file:
          content = template.read()
          file.write(content)



  def create_sg_group(self):
    self.init_sg_groups()
    
    # Open config file and get data
    with open(file="vars.tfvars.json", mode="r", encoding="utf-8") as file:
      content = json.load(file)
    
    name = input("Enter a name to the security group: ")
    description = input("Enter a description to the security group: ")

    # Check if the new security group name exists
    current_config = content["sg_config"]
    for sg in current_config:
      if sg["name"] == name:
        print("Name for security group already exists!")
        return

    content["sg_config"].append({
      "name": name,
      "description": description
    })

    with open(file="vars.tfvars.json", mode="w+", encoding="utf-8") as file:
      json.dump(obj=content, fp=file)

    os.system('terraform apply -auto-approve -var-file="vars.tfvars.json"')



  def delete_sg_group(self):
    with open(file="vars.tfvars.json", mode="r", encoding="utf-8") as file:
      content = json.load(file)
    name = input("\nEnter a name of the security group you want to delete: ")
    prev_config = content["sg_config"]
    new_config = []

    for sg in prev_config:
      if sg["name"] != name:
        new_config.append(sg)

    content["sg_config"] = new_config
    with open(file="vars.tfvars.json", mode="w+", encoding="utf-8") as file:
      json.dump(content, file)
    os.system('terraform apply -auto-approve -var-file="vars.tfvars.json"')
            

    
  def start_app(self):
    self.init_vpc()

    if (os.path.exists("./vars.tfvars.json") == False) and (os.path.exists("./instances.tf") == False):
      self.init_instances()

    while (1):
      try:
        command = input("\nIf you don't know the available commands, try help\n$ ")
        self.execute(command)
      except KeyboardInterrupt:
        print("\nStopping application...")
        time.sleep(1)
        break



  def execute(self, command: str):
    if (command in commands.keys()):
      if command == "help":
        self.help_command()
      elif command == "manage instances":
        self.manage_instances()
      elif command == "create sg":
        self.create_sg_group()
      elif command == "delete sg":
        self.delete_sg_group()
      elif command == "add sg to instance":
        self.set_sg_to_instance()
      # elif command == "delete instance":
      #   self.delete_instance()
      elif command == "create user":
        self.create_iam_user()
      elif command == "delete user":
        self.delete_user()
      elif command == "game over":
        self.destroy()
    else:
      print("\nInvalid command\n")



  def manage_instances(self):
    instance_type = input("Enter a type of the instances: ")
    instance_amount = input("Enter the number of the instances: ]")

    with open("vars.tfvars.json", mode="r", encoding="utf-8") as file:
      content = json.load(file)

    for instance in content["configuration"]:
      if instance["instance_type"] == instance_type:
        instance["no_of_instances"] = instance_amount

    with open(file="vars.tfvars.json", mode="w+", encoding="utf-8") as file:
      json.dump(content, file)
      
    os.system('terraform apply -auto-approve -var-file="vars.tfvars.json"')



  def set_sg_to_instance(self):
    instance_name = input("\nEnter the instance application name: ")
    sg_name       = input("Enter the security group name: ")

    sg_id = self.get_sg_id_by_name(sg_name)

    if sg_id is not None:
      with open("./vars.tfvars.json", mode="r", encoding="utf-8") as file:
        content = json.load(file)
      
      for instance in content["configuration"]:
        if (instance["application_name"] == instance_name) and (sg_id not in instance["vpc_security_group_ids"]):
          instance["vpc_security_group_ids"].append(sg_id)

          with open("./vars.tfvars.json", mode="w+", encoding="utf-8") as file:
            json.dump(content, file)

          os.system('terraform apply -auto-approve -var-file="vars.tfvars.json"')

          return

      print("Nada foi feito")
    else:
      print("Security group not found!")
    



  def create_iam_user(self):
    username = input("Enter the username to the new user: ")

    with open("./templates/users/user.tf", "r", encoding="utf-8") as template:
      with open("./new_user.tf", mode="w+", encoding="utf-8") as file:
        content = template.read()
        content = content.replace("var_iam_user_name", username)
        file.write(content)

    print(f"\nTerraform applying... Create user {username}")
    os.system("terraform apply -auto-approve")
    os.rename("./new_user.tf", f"user_{username}.tf")



  def delete_user(self):
    username = input("Enter the username to the new user: ")
    try:
      os.remove(f"user_{username}.tf")
      os.system("terraform apply -auto-approve")
    except:
      print("User not found")



  def help_command(self):
    print('\n---------------------------------------')
    print("You are able to execute these commands:\n")
    for command, action in commands.items():
      print(f"{command} - {action}")



  def get_sg_id_by_name(self, name: str):
    with open(file="./terraform.tfstate", mode="r", encoding="utf-8") as file:
      content = json.load(file)

    resources = content["resources"]
    for resource in resources:
      if (resource["type"] == "aws_security_group") and (resource["name"] == "terraform-sec-groups"):
        sg_instances = resource["instances"]
        for sg in sg_instances:
          if sg["index_key"] == name:
            return sg["attributes"]["id"]

    return None

  
  def destroy(self):
    print("\nDestroying the world...\n")
    os.system('terraform destroy -auto-approve -var-file="vars.tfvars.json"')
    os.remove("./vars.tfvars.json")
    os.remove("./instances.tf")
    try:
      os.remove("./security_groups.tf")
    except FileNotFoundError:
      pass


terraform_app = TerraformPy()
terraform_app.start_app()