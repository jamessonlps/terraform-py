variable "vpc_configuration" {
  type = object({
    cidr_block = string
  })

  default = {
    cidr_block = "172.16.0.0/16"
  }
}
