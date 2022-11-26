import json
import os

def read_tfstate():
  with open(file="terraform.tfstate", mode="r", encoding="utf-8") as file:
    content = json.load(file)
  return content


def read_vars():
  with open(file="vars.tfvars.json", mode="r", encoding="utf-8") as file:
    content = json.load(file)
  return content


def write_vars(content):
  with open(file="vars.tfvars.json", mode="w+", encoding="utf-8") as file:
    json.dump(content, file)


def terraform_apply():
  os.system('terraform apply -auto-approve -var-file="vars.tfvars.json"')


def terraform_destroy():
  os.system('terraform destroy -auto-approve -var-file="vars.tfvars.json"')