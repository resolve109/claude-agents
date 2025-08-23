# 🏗️ Infrastructure as Code Standards for Claude Agents

## Overview

This document defines the infrastructure standards and patterns that all Claude agents must follow, based on enterprise-grade patterns from the defaultLabs IaC repository.

## 🎯 Core Principles

### 1. **Security First**
- All infrastructure must be secure by default
- Implement defense-in-depth strategies
- Follow least privilege access principles
- Enable encryption at rest and in transit
- Implement comprehensive audit logging

### 2. **Reusability**
- Use modular, parameterized templates
- Create versioned, reusable modules
- Implement consistent naming conventions
- Follow DRY (Don't Repeat Yourself) principles

### 3. **Compliance Ready**
- SOC2, HIPAA, FEDRAMP compliance built-in
- Automated compliance scanning
- Security controls validation
- Audit trail maintenance

### 4. **Cost Optimization**
- FinOps practices embedded
- Resource tagging for cost allocation
- Auto-scaling and right-sizing
- Reserved instance planning

### 5. **Multi-Cloud Support**
- AWS and Azure native patterns
- Cloud-agnostic where possible
- Provider-specific optimizations

## 📋 Standard Template Structure

### CloudFormation (AWS)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: |
  Component: [Component Name]
  Purpose: [Clear description of what this deploys]
  Version: [Semantic version]
  Last Updated: [Date]
  Dependencies: [List any dependencies]
  Estimated Cost: [Monthly cost estimate]
  Features: [Key features list]

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: "Configuration Section Name"
        Parameters:
          - Parameter1
          - Parameter2
    ParameterLabels:
      Parameter1:
        default: "Human-Readable Label"

Parameters:
  # Environment Configuration
  Environment:
    Type: String
    Default: "dev"
    AllowedValues:
      - "dev"
      - "staging"
      - "prod"
    Description: "Deployment environment"
  
  # Naming Convention Parameters
  ProjectPrefix:
    Type: String
    Default: "default"
    Description: "Project prefix for resource naming"
    
  # Network Configuration
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: "VPC ID for deployment"
    
  # Security Configuration
  EnableEncryption:
    Type: String
    Default: "true"
    AllowedValues:
      - "true"
      - "false"
      
  # Cost Optimization
  InstanceType:
    Type: String
    Default: "t3.medium"
    AllowedValues:
      - "t3.small"
      - "t3.medium"
      - "t3.large"
      
Conditions:
  IsProduction: !Equals [!Ref Environment, "prod"]
  EnableEncryption: !Equals [!Ref EnableEncryption, "true"]

Mappings:
  EnvironmentConfig:
    dev:
      InstanceType: "t3.small"
      AutoScalingMin: 1
      AutoScalingMax: 3
    staging:
      InstanceType: "t3.medium"
      AutoScalingMin: 2
      AutoScalingMax: 5
    prod:
      InstanceType: "t3.large"
      AutoScalingMin: 3
      AutoScalingMax: 10

Resources:
  # Resources follow naming convention: ResourceTypeShortName
  
Outputs:
  # All outputs should be exported for cross-stack references
  OutputName:
    Description: "Description of output"
    Value: !Ref ResourceName
    Export:
      Name: !Sub "${AWS::StackName}-OutputName"
```

### Terraform (Azure/AWS)
```hcl
# ============================================
# Module: [Module Name]
# Purpose: [Clear description]
# Version: [Semantic version]
# ============================================

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# ============================================
# Variables
# ============================================

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_prefix" {
  description = "Project prefix for resource naming"
  type        = string
  default     = "default"
}

variable "location" {
  description = "Azure region or AWS region"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}

# ============================================
# Locals
# ============================================

locals {
  name_prefix = "${var.project_prefix}-${var.environment}"
  
  common_tags = merge(var.tags, {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project_prefix
    CreatedAt   = timestamp()
  })
  
  # Environment-specific configurations
  env_config = {
    dev = {
      instance_type = "t3.small"
      min_capacity  = 1
      max_capacity  = 3
    }
    staging = {
      instance_type = "t3.medium"
      min_capacity  = 2
      max_capacity  = 5
    }
    prod = {
      instance_type = "t3.large"
      min_capacity  = 3
      max_capacity  = 10
    }
  }
}

# ============================================
# Data Sources
# ============================================

data "azurerm_client_config" "current" {}

# ============================================
# Resources
# ============================================

# Resources follow naming convention

# ============================================
# Outputs
# ============================================

output "resource_id" {
  description = "Resource identifier"
  value       = azurerm_resource.example.id
  sensitive   = false
}
```

## 🔧 Naming Conventions

### AWS Resources
```
{service}-{project}-{environment}-{region}-{description}
Examples:
- s3-default-prod-use1-backups
- ec2-default-dev-usw2-webserver
- rds-default-staging-use1-postgres
```

### Azure Resources
```
{resourcetype}-{project}-{environment}-{location}-{description}
Examples:
- rg-default-prod-eus-main
- st-default-dev-wus-data
- vm-default-staging-eus-web
```

### Tags/Labels (Required)
```yaml
Environment: dev|staging|prod
Project: project-name
Owner: team-name
CostCenter: cost-center-code
ManagedBy: Terraform|CloudFormation
CreatedAt: timestamp
Purpose: description
Compliance: SOC2|HIPAA|FEDRAMP|None
DataClassification: Public|Internal|Confidential|Restricted
```

## 🔐 Security Standards

### Encryption Requirements
- **At Rest**: All storage must be encrypted
- **In Transit**: TLS 1.2 minimum
- **Key Management**: Use KMS/Key Vault with rotation

### Network Security
```yaml
# Default Security Group Rules
Ingress:
  - HTTPS (443): From ALB only
  - SSH (22): From Bastion only (prod)
  - Application Ports: From internal subnets only
  
Egress:
  - HTTPS (443): To internet (for updates)
  - Database Ports: To data subnet only
  - NTP (123): To time servers
```

### Secret Management
```yaml
# Never hardcode secrets
Secrets:
  Storage: AWS Secrets Manager | Azure Key Vault
  Rotation: Enabled with 30-day rotation
  Access: IAM/RBAC controlled
  Audit: All access logged
```

## 📊 CI/CD Pipeline Standards

### GitLab CI Template
```yaml
stages:
  - validate
  - security-scan
  - test
  - build
  - deploy-dev
  - deploy-staging
  - deploy-prod

variables:
  TF_ROOT: ${CI_PROJECT_DIR}/terraform
  DOCKER_DRIVER: overlay2
  FF_USE_FASTZIP: "true"

include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

.base_job:
  tags:
    - docker
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure

validate:
  extends: .base_job
  stage: validate
  script:
    - terraform fmt -check
    - terraform validate
    - checkov -f .

security-scan:
  extends: .base_job
  stage: security-scan
  script:
    - trivy fs --severity HIGH,CRITICAL .
    - tfsec .
```

### GitHub Actions Template
```yaml
name: Infrastructure Deployment

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  TF_VERSION: "1.5.0"
  
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: ${{ env.TF_VERSION }}
      - run: terraform fmt -check
      - run: terraform validate
      
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
```

## 💰 Cost Optimization Patterns

### Auto-Scaling Configuration
```yaml
AutoScaling:
  Metrics:
    - CPU: 70% threshold
    - Memory: 80% threshold
    - Request Count: Based on baseline
  
  Scaling:
    ScaleUp:
      Cooldown: 300 seconds
      Increment: 1 instance
    ScaleDown:
      Cooldown: 600 seconds
      Decrement: 1 instance
  
  Limits:
    Dev: min=1, max=3
    Staging: min=2, max=5
    Prod: min=3, max=10
```

### Resource Tagging for Cost Allocation
```yaml
CostTags:
  Required:
    - Environment
    - Project
    - Owner
    - CostCenter
  Optional:
    - Application
    - Team
    - ExpiryDate
```

## 🚀 Module Structure

### Standard Module Layout
```
module/
├── README.md           # Module documentation
├── main.tf            # Main resource definitions
├── variables.tf       # Input variables
├── outputs.tf         # Output values
├── data.tf           # Data sources
├── locals.tf         # Local values
├── versions.tf       # Provider requirements
├── examples/         # Usage examples
│   ├── basic/
│   └── advanced/
└── tests/           # Module tests
    ├── unit/
    └── integration/
```

### Module Versioning
```
Semantic Versioning: MAJOR.MINOR.PATCH

v1.0.0 - Initial stable release
v1.1.0 - New feature (backward compatible)
v1.0.1 - Bug fix
v2.0.0 - Breaking change
```

## 📋 Compliance Checklists

### SOC2 Compliance
- [ ] Encryption at rest enabled
- [ ] Encryption in transit enabled
- [ ] Access logging enabled
- [ ] Audit trails configured
- [ ] MFA enforced
- [ ] Regular security assessments

### HIPAA Compliance
- [ ] PHI data encrypted
- [ ] Access controls implemented
- [ ] Audit logs retained for 6 years
- [ ] Business Associate Agreements
- [ ] Incident response plan

### FEDRAMP Compliance
- [ ] Continuous monitoring
- [ ] Vulnerability scanning
- [ ] Configuration baselines
- [ ] Security control testing
- [ ] Authorization boundaries defined

## 🔄 Disaster Recovery Standards

### Backup Strategy
```yaml
Backup:
  Frequency:
    Dev: Daily
    Staging: Every 12 hours
    Prod: Every 6 hours
  
  Retention:
    Dev: 7 days
    Staging: 14 days
    Prod: 30 days
  
  Testing:
    Frequency: Monthly
    Procedure: Full restore test
```

### RTO/RPO Targets
```yaml
Environments:
  Dev:
    RTO: 24 hours
    RPO: 24 hours
  Staging:
    RTO: 4 hours
    RPO: 12 hours
  Prod:
    RTO: 1 hour
    RPO: 15 minutes
```

## 🎯 Implementation Checklist

When creating or updating infrastructure:

### Pre-Deployment
- [ ] Follow naming conventions
- [ ] Implement proper tagging
- [ ] Security scan passed
- [ ] Cost estimate reviewed
- [ ] Compliance requirements met

### Deployment
- [ ] Use CI/CD pipeline
- [ ] Environment-specific configs
- [ ] Automated testing
- [ ] Approval gates for prod

### Post-Deployment
- [ ] Monitoring configured
- [ ] Alerts set up
- [ ] Documentation updated
- [ ] Cost tracking enabled
- [ ] Security validation

## 📚 Agent-Specific Standards

### When agents generate infrastructure code:

1. **Always use parameterized templates**
2. **Include comprehensive descriptions**
3. **Follow security-first approach**
4. **Implement cost optimization**
5. **Add monitoring and logging**
6. **Include disaster recovery**
7. **Document dependencies**
8. **Provide usage examples**
9. **Include validation logic**
10. **Generate with compliance in mind**

### Example Output Structure
```yaml
# Agent-generated infrastructure should include:
- Template file (main configuration)
- Variables file (parameterized inputs)
- Outputs file (resource outputs)
- README with:
  - Purpose and description
  - Prerequisites
  - Usage examples
  - Cost estimates
  - Security considerations
  - Compliance notes
```

## 🔗 References

- AWS Well-Architected Framework
- Azure Well-Architected Framework
- Terraform Best Practices
- CloudFormation Best Practices
- CIS Benchmarks
- NIST Cybersecurity Framework

---

**Note**: These standards are based on production-grade patterns for enterprise infrastructure and should be followed by all Claude agents when generating or reviewing infrastructure code.