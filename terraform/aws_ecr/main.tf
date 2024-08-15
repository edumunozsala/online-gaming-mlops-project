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
  region     = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY  
}

resource "aws_ecr_repository" "container_repository" {
  name                 = "${var.app_name}-${var.app_environment}-repository"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "${var.app_name}-repository"
    Environment = var.app_environment
  }

  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_ecr_repository" "tracker_repository" {
  name                 = "${var.tracker_name}-repository"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "${var.tracker_name}-repository"
    Environment = var.app_environment
  }

  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_ecr_repository" "reporter_repository" {
  name                 = "${var.reporter_name}-repository"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "${var.reporter_name}-repository"
    Environment = var.app_environment
  }

  lifecycle {
    prevent_destroy = false
  }
}

output "container_repository_url" {
  value = "http://${aws_ecr_repository.container_repository.repository_url}"
}

output "container_registry_id" {
  value = "http://${aws_ecr_repository.container_repository.registry_id}"
}
