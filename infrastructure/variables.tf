variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "eu-north-1"
}

variable "ami_id" {
  description = "AMI ID for Ubuntu 22.04 LTS. Update this if you change region."
  type        = string
  default     = "ami-0a664360bb4a53714"
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.micro"
}

variable "key_pair_name" {
  description = "Name of an existing EC2 key pair for SSH access"
  type        = string
  # No default — user must supply this
}
