# AWS Documentation Database

This directory contains a comprehensive database of AWS service documentation URLs and metadata for use by all Claude agents.

## Structure

```
aws-docs/
├── services-master.json     # Master database with all service information
├── categories-index.json    # Index by service categories
├── tags-index.json          # Index by service tags
└── README.md               # This file
```

## Quick Start

### For Shell Scripts

```bash
# Get documentation URL for a service
/mnt/e/github/agents/claude-agents/.claude/data/scripts/aws-docs-lookup.sh service lambda

# List all services in a category
/mnt/e/github/agents/claude-agents/.claude/data/scripts/aws-docs-lookup.sh category compute

# Search for services
/mnt/e/github/agents/claude-agents/.claude/data/scripts/aws-docs-lookup.sh search container
```

### For Python Scripts

```python
from pathlib import Path
import sys
sys.path.append('/mnt/e/github/agents/claude-agents/.claude/data/scripts')
from aws_docs_api import AWSDocsAPI

# Initialize API
api = AWSDocsAPI()

# Get service URL
url = api.get_service_url('lambda')

# Search services
results = api.search_services('serverless')

# Get services by category
compute_services = api.get_services_by_category('compute')
```

### Direct JSON Access

```bash
# Using jq to query the master database
jq '.services.lambda.pdf_url' /mnt/e/github/agents/claude-agents/.claude/data/aws-docs/services-master.json

# Get all services in a category
jq '.categories.compute.services' /mnt/e/github/agents/claude-agents/.claude/data/aws-docs/categories-index.json

# Get all services with a tag
jq '.tags.serverless' /mnt/e/github/agents/claude-agents/.claude/data/aws-docs/tags-index.json
```

## Available Commands

### Shell Script (aws-docs-lookup.sh)

- `service <name>` - Get PDF URL for a specific service
- `category <name>` - List all services in a category
- `tag <name>` - List all services with a specific tag
- `list` - List all available services
- `list-categories` - List all available categories
- `list-tags` - List all available tags
- `search <term>` - Search for services
- `info <service>` - Get detailed service information

### Python API (aws_docs_api.py)

- `get_service_url(service)` - Get PDF URL for a service
- `get_service_info(service)` - Get complete service information
- `list_all_services()` - List all service identifiers
- `get_services_by_category(category)` - Get services in a category
- `get_services_by_tag(tag)` - Get services with a tag
- `search_services(term)` - Search for services
- `get_terraform_resources(service)` - Get Terraform resource mappings

## Service Categories

- **compute** - EC2, Lambda, Auto Scaling, Batch, Lightsail, Elastic Beanstalk
- **containers** - ECS, EKS, ECR, Fargate
- **networking** - VPC, ELB, CloudFront, Route 53, Direct Connect, API Gateway
- **storage** - S3, EFS, FSx, EBS, Backup, Storage Gateway
- **database** - RDS, DynamoDB, ElastiCache, Aurora, DocumentDB, Neptune
- **security** - IAM, WAF, KMS, Secrets Manager, GuardDuty, ACM, Cognito
- **management** - CloudFormation, SAM, CDK, Systems Manager, Organizations
- **monitoring** - CloudWatch, X-Ray, CloudTrail
- **devops** - CodePipeline, CodeBuild, CodeDeploy
- **integration** - SQS, SNS, EventBridge, Step Functions, MQ
- **analytics** - Redshift, Athena, EMR, Kinesis, Glue, MSK
- **migration** - DMS, DataSync, Transfer Family, Migration Hub
- **billing** - Cost Explorer, Budgets, Cost and Usage Report
- **hybrid** - Outposts, Wavelength, Local Zones
- **ml** - SageMaker
- **media** - Media Services

## Common Tags

- `serverless` - Lambda, DynamoDB, API Gateway, SAM, Fargate, etc.
- `containers` - ECS, EKS, ECR, Fargate, Batch
- `iac` - CloudFormation, SAM, CDK
- `security` - IAM, WAF, KMS, GuardDuty, Security Hub, etc.
- `monitoring` - CloudWatch, X-Ray, CloudTrail
- `cicd` - CodePipeline, CodeBuild, CodeDeploy
- `database` - RDS, DynamoDB, Aurora, DocumentDB, etc.
- `networking` - VPC, ELB, CloudFront, Route 53, etc.
- `big-data` - EMR, Kinesis, Glue, Athena, Redshift
- `cost-optimization` - Cost Explorer, Budgets, Auto Scaling, Lambda

## Integration with Agents

### For the AWS Agent

```bash
# In AWS agent scripts
source /mnt/e/github/agents/claude-agents/.claude/data/scripts/aws-docs-lookup.sh
get_service_url "ec2"
```

### For the Terraform Agent

```python
# In Terraform agent scripts
from aws_docs_api import AWSDocsAPI
api = AWSDocsAPI()

# Get Terraform resource mappings
resources = api.get_terraform_resources('ec2')
# Returns: {'aws_instance': 'EC2 instance', 'aws_security_group': 'Security group', ...}
```

### For the CICD Agent

```bash
# Quick reference for pipeline services
./aws-docs-lookup.sh tag cicd
```

## Statistics

- **Total Services**: 85
- **Categories**: 16
- **Unique Tags**: 40+
- **Last Updated**: 2025-08-23

## Maintenance

To update the documentation URLs:

1. Edit `/mnt/e/github/agents/claude-agents/.claude/data/aws-docs/services-master.json`
2. Update the relevant category in `categories-index.json` if adding new services
3. Update the tags in `tags-index.json` for cross-cutting concerns
4. Test using the lookup scripts to ensure data integrity

## Examples

### Get Lambda Documentation
```bash
$ ./aws-docs-lookup.sh service lambda
AWS Lambda
PDF URL: https://docs.aws.amazon.com/pdfs/lambda/latest/dg/lambda-dg.pdf
Category: compute
Tags: serverless, functions, event-driven
```

### Find All Serverless Services
```bash
$ ./aws-docs-lookup.sh tag serverless
Tag: serverless

Services:
  lambda - AWS Lambda
    URL: https://docs.aws.amazon.com/pdfs/lambda/latest/dg/lambda-dg.pdf
  dynamodb - Amazon DynamoDB
    URL: https://docs.aws.amazon.com/pdfs/amazondynamodb/latest/developerguide/dynamodb-dg.pdf
  apigateway - Amazon API Gateway
    URL: https://docs.aws.amazon.com/pdfs/apigateway/latest/developerguide/apigateway-dg.pdf
  ...
```

### Search for Container Services
```python
from aws_docs_api import AWSDocsAPI
api = AWSDocsAPI()

results = api.search_services('container')
for service in results:
    print(f"{service['id']}: {service['name']}")
    print(f"  URL: {service['pdf_url']}")
```

## Support

For issues or questions about the AWS documentation database:
1. Check this README first
2. Review the data files directly in JSON format
3. Use the search functionality to find related services
4. Contact the Claude Master agent for assistance