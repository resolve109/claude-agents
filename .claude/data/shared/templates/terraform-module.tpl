# Terraform Module Template
# Usage: Copy this template and customize for your specific module

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Module Variables
variable "module_name" {
  description = "Name of this module instance"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}

# Local Values
locals {
  common_tags = merge(
    var.tags,
    {
      Module      = var.module_name
      Environment = var.environment
      ManagedBy   = "Terraform"
      CreatedAt   = timestamp()
    }
  )
}

# Resources
# Add your resources here

# Outputs
output "module_id" {
  description = "Unique identifier for this module instance"
  value       = "${var.module_name}-${var.environment}"
}

output "tags" {
  description = "Tags applied to resources"
  value       = local.common_tags
}