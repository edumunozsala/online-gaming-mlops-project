variable "AWS_ACCESS_KEY_ID" {
  type    = string
}

variable "AWS_SECRET_ACCESS_KEY" {
  type    = string
}

variable "AWS_REGION" {
  type        = string
  description = "AWS Region"
}

variable "AWS_BUCKET_NAME" {
  type        = string
  description = "S3 bucket for our project"
}

variable "MYLOCALIP" {
  description = "The IP address to access from."
}


variable "PROJECT_NAME" {
  type        = string
  description = "Mage project"
  default     = "machine_learning"
}

variable "default_s3_content" {
   description = "The default content of the s3 bucket upon creation of the bucket"
   type = set(string)
   default = ["input", "processed", "batch", "batch/output", "monitoring","monitoring/reference", "monitoring/current", "monitoring/reports", "mlflow"]
}

variable "app_name" {
  type        = string
  description = "Application Name"
  default     = "online-gaming"
}

variable "app_environment" {
  type        = string
  description = "Application Environment"
  default     = "production"
}

variable "docker_image" {
  description = "Docker image url used in ECS task."
  default     = "223817798831.dkr.ecr.us-west-2.amazonaws.com/online-gaming-production-repository:latest"
  type        = string
}

variable "database_user" {
  type        = string
  description = "The username of the Postgres database."
  default     = "mageuser"
}

variable "database_password" {
  type        = string
  description = "The password of the Postgres database."
  sensitive   = true
}

variable "ecs_task_cpu" {
  description = "ECS task cpu"
  default     = 2048
}

variable "ecs_task_memory" {
  description = "ECS task memory"
  default     = 8192
}

variable "public_subnets" {
  description = "List of public subnets"
  default     = ["10.32.100.0/24", "10.32.101.0/24"]
}

variable "private_subnets" {
  description = "List of private subnets"
  default     = ["10.32.0.0/24", "10.32.1.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones"
  default     = ["us-west-2a", "us-west-2b"]
}

variable "enable_ci_cd" {
  description = "A flag to enable/disable the CI/CD null resource"
  type        = bool
  default     = false
}

variable "cidr" {
  description = "The CIDR block for the VPC."
  default     = "10.32.0.0/16"
}

variable "tracker_name" {
  type        = string
  description = "Experiment Tracking tool Name"
  default     = "mlflow"
}

variable "tracker_image" {
  description = "Docker image url used in ECS task for Mlflow server."
  default     = "223817798831.dkr.ecr.us-west-2.amazonaws.com/mlflow-repository:latest"
  type        = string
}

variable "tracker_task_cpu" {
  description = "ECS task cpu"
  default     = 1024
}

variable "tracker_task_memory" {
  description = "ECS task memory"
  default     = 4096
}

variable "reporting_name" {
  type        = string
  description = "Experiment Tracking tool Name"
  default     = "report-server"
}

variable "reporting_image" {
  description = "Docker image url used in ECS task for Mlflow server."
  default     = "223817798831.dkr.ecr.us-west-2.amazonaws.com/report-server-repository:latest"
  type        = string
}

variable "reporting_task_cpu" {
  description = "ECS task cpu"
  default     = 512
}

variable "reporting_task_memory" {
  description = "ECS task memory"
  default     = 2048
}
