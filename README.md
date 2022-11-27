# Virtual Private Cloud

---

## Building a Virtual Private Cloud with AWS and Terraform

This repository is a Cloud Computing project that implements a VPC on AWS using Infrastructure as a Code (IaaC), using python scripts to manipulate the infrastructure.

In the VPC created here, you will be able to:

- [x]  Increase and decrease the number of instances
- [x]  Create an IAM User
- [x]  Delete an IAM User
- [x]  Create a security group and associate it with instances
- [x]  Delete a secutiry group
- [x]  List all instances, users, security groups and its rules.

## How to execute this project

**Install Terraform**

First, you need to install **Terraform** on your machine. The [official page](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) contains all the necessary instructions for each OS.

Also, you will need to register with AWS. Write down your *secret_key* and your *access_key*.

**Setting AWS credentials**

You must export your credentials. They will not be stored in the code.

```powershell
$ export AWS_ACCESS_KEY_ID="anaccesskey"
$ export AWS_SECRET_ACCESS_KEY="asecretkey"
$ export AWS_REGION="us-west-2"
```

**Initializing**

All operations will be performed via command line. To get started, from the project root, run:

```powershell
$ python3 ./main.py
```

The application will then start creating the entire base infrastructure, that is, the VPC, internet gateway, route table, etc. To see the command possibilities, run `help`.

Commands

- `help` -
- `manage instances` -
- `create user` -
- `delete user` -
- `create sg` -
- `delete sg` -
- `add sg to instance` -