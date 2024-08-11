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

variable "tracker_name" {
  type        = string
  description = "Experiment Tracking tool Name"
  default     = "mlflow"
}

variable "reporter_name" {
  type        = string
  description = "Experiment Tracking tool Name"
  default     = "report-server"
}