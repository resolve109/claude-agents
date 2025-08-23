# AWS Documentation System - Quick Start Guide

## For All Agents

The AWS documentation system is now available at:
`/mnt/e/github/agents/claude-agents/.claude/data/shared/references/aws-docs/`

## Quick Commands

### 1. Search for a Service
```bash
python3 .claude/data/scripts/aws-docs-lookup.py search <term>
# Example: python3 .claude/data/scripts/aws-docs-lookup.py search lambda
```

### 2. Get Service Information
```bash
python3 .claude/data/scripts/aws-docs-lookup.py service <service-name>
# Example: python3 .claude/data/scripts/aws-docs-lookup.py service ec2
```

### 3. List Services by Category
```bash
python3 .claude/data/scripts/aws-docs-lookup.py category <category-name>
# Example: python3 .claude/data/scripts/aws-docs-lookup.py category networking
```

### 4. Download Documentation
```bash
python3 .claude/data/scripts/aws-docs-converter.py service <service-name>
# Example: python3 .claude/data/scripts/aws-docs-converter.py service s3
```

## Direct JSON Access

### Master Index (All Services)
```python
import json
with open('.claude/data/shared/references/aws-docs/master-index.json') as f:
    aws_docs = json.load(f)
    
# Get EC2 documentation URL
ec2_url = aws_docs['services']['ec2']['pdf_url']
```

### Category Indexes (Detailed Info)
Available category files:
- `core-infrastructure.json` - EC2, ECS, EKS, Lambda, API Gateway
- `networking.json` - VPC, ELB, CloudFront, Route 53, Direct Connect
- `databases.json` - RDS, Aurora, DynamoDB, ElastiCache, etc.
- `security.json` - IAM, WAF, KMS, Secrets Manager, GuardDuty, etc.

## Service Count by Category

| Category | Services | Key Examples |
|----------|----------|--------------|
| Core Infrastructure | 5 | EC2, Lambda, EKS |
| Networking | 5 | VPC, CloudFront, Route 53 |
| Storage | 6 | S3, EFS, EBS |
| Databases | 7 | RDS, DynamoDB, Aurora |
| Security | 10 | IAM, KMS, WAF |
| IaC & Automation | 7 | CloudFormation, CDK, SAM |
| Monitoring | 3 | CloudWatch, X-Ray |
| CI/CD | 4 | CodePipeline, CodeBuild |
| Messaging | 8 | SQS, SNS, EventBridge |
| Analytics | 5 | Athena, Kinesis, Glue |
| Management | 5 | Organizations, Control Tower |
| **Total** | **81** | **All AWS Services** |

## Integration for Agents

### For Terraform Agent
```bash
# Get infrastructure service docs
python3 .claude/data/scripts/aws-docs-lookup.py category core-infrastructure
python3 .claude/data/scripts/aws-docs-lookup.py category iac-automation
```

### For AWS Agent
```bash
# Get all AWS service information
python3 .claude/data/scripts/aws-docs-lookup.py list-services
python3 .claude/data/scripts/aws-docs-lookup.py stats
```

### For Security Agent
```bash
# Get security-related documentation
python3 .claude/data/scripts/aws-docs-lookup.py category security
python3 .claude/data/scripts/aws-docs-lookup.py service iam
```

### For Kubernetes Agent
```bash
# Get container and Kubernetes docs
python3 .claude/data/scripts/aws-docs-lookup.py service eks
python3 .claude/data/scripts/aws-docs-lookup.py service ecs
python3 .claude/data/scripts/aws-docs-lookup.py service fargate
```

## Using the Integration Script

Source the integration script for quick functions:
```bash
source .claude/data/shared/references/aws-docs-integration.sh

# Then use shortcuts:
aws-service ec2
aws-category networking
aws-search lambda
aws-doc-get s3
```

## MCP Server Integration

If MCP servers are available:
- **fetch**: Can download PDFs directly
- **mdconvert**: Can convert PDFs to markdown
- **filesystem**: Can manage documentation files

## Notes

- Documentation URLs are official AWS PDF links
- PDFs are large (10-50MB each) - download on demand
- Text conversion available via Python script
- All 81 major AWS services are indexed
- System supports offline documentation access once downloaded

## File Locations

- **Master Index**: `.claude/data/shared/references/aws-docs/master-index.json`
- **Category Indexes**: `.claude/data/shared/references/aws-docs/indexes/*.json`
- **Lookup Script**: `.claude/data/scripts/aws-docs-lookup.py`
- **Converter Script**: `.claude/data/scripts/aws-docs-converter.py`
- **Integration Helper**: `.claude/data/shared/references/aws-docs-integration.sh`

## Support

For issues or updates to the documentation system, consult the Claude Master agent or modify the master-index.json file directly.