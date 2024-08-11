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

variable "default_s3_content" {
   description = "The default content of the s3 bucket upon creation of the bucket"
   type = set(string)
   default = ["input", "processed", "batch", "batch/output", "monitoring","monitoring/reference", "monitoring/current", "monitoring/reports", "mlflow"]
}
