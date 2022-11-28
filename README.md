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
- [x]  Create and delete rules for the security groups.

## How to execute this project

**Install Terraform**

First, you need to install **Terraform** on your machine. The [official page](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) contains all the necessary instructions for each OS.

**Install AWS CLI**

Follow [this tutorial](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html) for your operating system. Also, you will need to register with AWS. Write down your *secret_key* and your *access_key*.

**Setting AWS credentials**

You must export your credentials. They will not be stored in the code.

```powershell
$ export AWS_ACCESS_KEY_ID="anaccesskey"
$ export AWS_SECRET_ACCESS_KEY="asecretkey"
$ export AWS_REGION="us-east-1"
```

**Initializing**

All operations will be performed via command line. To get started, from the project root, run:

```powershell
$ python3 ./main.py
```

The application will then start creating the entire base infrastructure, that is, the VPC, internet gateway, route table, etc. To see the command possibilities, run `help`.

**Commands**

- `help` - See all commands
- `manage instances` - Increase or decrease instances
- `create user` - Create an new user
- `delete user` - Delete an user
- `create sg` - Create a new security group
- `delete sg` - Delete a security group
- `create rule` - Create a rule to the security group
- `delete rule` - Delete a rule of the security group
- `add sg to instance` - Associate the security group to a group of instances