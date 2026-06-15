variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "name" {
  description = "Name prefix for resources"
  type        = string
  default     = "ecs-sandbox"
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
  default     = 8080
}

variable "desired_count" {
  description = "Number of running tasks"
  type        = number
  default     = 2
}

variable "image_tag" {
  description = "Container image tag to deploy"
  type        = string
  default     = "latest"
}

variable "cpu" {
  description = "Fargate task CPU units"
  type        = number
  default     = 256
}

variable "memory" {
  description = "Fargate task memory (MiB)"
  type        = number
  default     = 512
}

variable "db_name" {
  description = "Initial PostgreSQL database name"
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "PostgreSQL master username"
  type        = string
  default     = "appuser"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t4g.micro"
}
