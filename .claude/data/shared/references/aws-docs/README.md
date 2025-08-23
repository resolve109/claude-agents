# AWS Documentation Reference System

## Overview
This directory contains a comprehensive reference system for AWS service documentation, making it easy for all Claude agents to access AWS service information, documentation URLs, and converted text files.

## Directory Structure
```
aws-docs/
├── README.md                 # This file
├── master-index.json         # Complete index of all AWS services
├── indexes/                  # Category-specific indexes with detailed information
│   ├── core-infrastructure.json
│   ├── networking.json
│   ├── databases.json
│   ├── security.json
│   └── ...
├── pdfs/                     # Downloaded PDF documentation (populated on demand)
├── text/                     # Converted text files from PDFs (populated on demand)
└── cache/                    # Cache directory for temporary files
```

## Available Tools

### 1. Python Lookup Tool (Recommended)
Location: `/mnt/e/github/agents/claude-agents/.claude/data/scripts/aws-docs-lookup.py`

**Commands:**
```bash
# Get information about a specific service
python3 aws-docs-lookup.py service ec2

# List all services in a category
python3 aws-docs-lookup.py category networking

# Search for services
python3 aws-docs-lookup.py search lambda

# List all categories
python3 aws-docs-lookup.py list-categories

# List all services
python3 aws-docs-lookup.py list-services

# Show statistics
python3 aws-docs-lookup.py stats
```

### 2. Python Converter Tool
Location: `/mnt/e/github/agents/claude-agents/.claude/data/scripts/aws-docs-converter.py`

**Commands:**
```bash
# Download and convert a single service
python3 aws-docs-converter.py service ec2

# Process entire category
python3 aws-docs-converter.py category networking

# Process all services
python3 aws-docs-converter.py all

# Show status of all services
python3 aws-docs-converter.py status

# Download only (no conversion)
python3 aws-docs-converter.py service ec2 --download-only

# Convert only (from existing PDFs)
python3 aws-docs-converter.py service ec2 --convert-only
```

### 3. Bash Lookup Script (requires jq)
Location: `/mnt/e/github/agents/claude-agents/.claude/data/scripts/aws-docs-lookup.sh`

**Note:** This script requires `jq` to be installed. Use the Python version if `jq` is not available.

## Quick Access Examples

### For Terraform Agent
```python
# Access infrastructure services
import json
with open('.claude/data/shared/references/aws-docs/indexes/core-infrastructure.json') as f:
    infra_services = json.load(f)
    ec2_info = infra_services['services']['ec2']
    print(f"EC2 Documentation: {ec2_info['pdf_url']}")
```

### For AWS Agent
```python
# Get all services in a category
import json
with open('.claude/data/shared/references/aws-docs/master-index.json') as f:
    index = json.load(f)
    networking = index['categories']['networking']['services']
    for service in networking:
        print(f"{service}: {index['services'][service]['pdf_url']}")
```

### For Security Agent
```python
# Access security services
import json
with open('.claude/data/shared/references/aws-docs/indexes/security.json') as f:
    security_services = json.load(f)
    iam_topics = security_services['services']['iam']['key_topics']
    print("IAM Key Topics:", iam_topics)
```

## Service Categories

1. **Core Infrastructure** (5 services)
   - EC2, ECS, EKS, Lambda, API Gateway

2. **Networking & Load Balancing** (5 services)
   - VPC, ELB, CloudFront, Route 53, Direct Connect

3. **Storage** (6 services)
   - S3, EFS, FSx, EBS, Backup, Storage Gateway

4. **Databases** (7 services)
   - RDS, Aurora, DynamoDB, ElastiCache, DocumentDB, Neptune, Redshift

5. **Security & Identity** (10 services)
   - IAM, WAF, KMS, Secrets Manager, GuardDuty, ACM, Cognito, Inspector, Macie, Security Hub

6. **Infrastructure as Code & Automation** (7 services)
   - CloudFormation, SAM, CDK, Systems Manager, Auto Scaling, OpsWorks, AppConfig

7. **Monitoring & Observability** (3 services)
   - CloudWatch, X-Ray, CloudTrail

8. **CI/CD & Developer Tools** (4 services)
   - CodePipeline, CodeBuild, CodeDeploy, ECR

9. **Messaging & Integration** (8 services)
   - SQS, SNS, EventBridge, Step Functions, App Mesh, MQ, AppFlow, API Gateway V2

10. **Container Services** (2 services)
    - Fargate, Batch

11. **Analytics & Big Data** (5 services)
    - Athena, EMR, Kinesis, Glue, MSK

12. **Management & Governance** (5 services)
    - Organizations, Config, Service Catalog, Control Tower, RAM

13. **Migration & Transfer** (4 services)
    - DMS, DataSync, Transfer Family, Migration Hub

14. **Cost Management** (3 services)
    - Cost Explorer, Budgets, Cost and Usage Report

15. **Hybrid & Edge** (3 services)
    - Outposts, Wavelength, Local Zones

16. **Additional Compute** (2 services)
    - Lightsail, Elastic Beanstalk

17. **Machine Learning Infrastructure** (1 service)
    - SageMaker

18. **Media Services** (1 service)
    - Media Services

## Total Services Indexed: 81

## Using with MCP Servers

The system is designed to work with MCP servers when available:

1. **mdconvert**: Can be used for PDF to markdown conversion
2. **fetch**: Can download PDFs from AWS documentation URLs
3. **filesystem**: Can manage the local file structure

## Integration with Agents

All agents can access this documentation system. The recommended approach:

1. Use the master-index.json for quick URL lookups
2. Use category indexes for detailed service information
3. Use the converter scripts to download and process documentation on demand
4. Store frequently accessed text files in the text/ directory

## Updating Documentation

To update the documentation URLs or add new services:

1. Edit the master-index.json file
2. Update the relevant category index files
3. Run the converter script to download new PDFs
4. Commit changes to version control

## Notes

- PDFs are large files (often 10-50 MB each)
- Download PDFs on demand rather than all at once
- Text conversion quality varies by PDF structure
- Some services may have multiple documentation guides
- URLs are current as of August 2024 and may need periodic updates

## Support

For issues or questions about this documentation system, consult:
- The Claude Master agent (CLAUDE.md)
- The AWS agent for AWS-specific queries
- The Terraform agent for infrastructure documentation needs