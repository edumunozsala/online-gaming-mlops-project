terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.50"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region     = "${var.AWS_REGION}"
  access_key = "${var.AWS_ACCESS_KEY_ID}"
  secret_key = "${var.AWS_SECRET_ACCESS_KEY}"
}

resource "aws_s3_bucket" "project_bucket" {
  bucket = "${var.AWS_BUCKET_NAME}"

  tags = {
    Name        = "project"
    Environment = "mlops-online"
  }
}

resource "aws_s3_object" "default_s3_content" {
    for_each = var.default_s3_content
    bucket = aws_s3_bucket.project_bucket.id
    key = "${each.value}/"
}

