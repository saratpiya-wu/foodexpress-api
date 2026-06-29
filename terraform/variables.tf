variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-southeast-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Name of an existing AWS EC2 Key Pair (for SSH access)"
  type        = string
}

variable "docker_image" {
  description = "Docker image to run on the instance, e.g. yourdockerhubuser/foodexpress:latest"
  type        = string
}
