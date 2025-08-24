# Claude Code Agents for DevOps & Infrastructure Teams

## CRITICAL: File Location Architecture

### .claude Directory = Claude's Internal Operations ONLY
**THIS IS A FUNDAMENTAL RULE: The `.claude` folder is EXCLUSIVELY for Claude's internal workspace.**

#### What belongs in .claude:
- Agent definitions (`.claude/agents/*.md`)
- Self-optimization scripts (`.claude/scripts/*.py`)
- MCP configurations (`.claude/mcp/`)
- Internal references and data
- Claude's operational files

#### What NEVER belongs in .claude:
- User task deliverables
- Project code files
- Infrastructure configurations (unless they're agent templates)
- Any files the user requests be created

### User Files = ALWAYS Outside .claude
When creating files for users:
1. **Default location**: Project root directory
2. **Organized locations**: `/terraform`, `/kubernetes`, `/cloudformation`, etc.
3. **User-specified**: Ask if uncertain
4. **NEVER**: Inside `.claude` directory

### Self-Check Protocol (MANDATORY)
```python
def validate_file_location(file_path):
    if '.claude/' in file_path:
        if not is_internal_claude_operation():
            raise ValueError("STOP! User files cannot be saved in .claude directory!")
            # Redirect to appropriate location
            return get_proper_user_file_location(file_path)
    return file_path  # Safe to proceed
```

## Token Optimization Guidelines

### CRITICAL: Reduce Token Usage (Target: <30% of limit)

#### Agent Definition Best Practices
- **Max 200 lines per agent** (reduced from 500+)
- **Use shorthand notation**: `→` instead of verbose descriptions
- **Remove examples from descriptions** - keep in separate docs
- **Compress YAML/JSON** to single-line where possible
- **Use abbreviations**: K8s, TF, IaC, CICD, etc.

#### Smart Data Access Patterns
- **Summary-first approach**: Read metadata before full content
- **Hash-based lookups**: Use MASTER_INDEX.json for quick references
- **Chunked reading**: Only load relevant sections
- **Cache frequently used data**: Store in compressed format
- **Lazy loading**: Don't preload entire files

#### Response Efficiency
- **Progressive disclosure**: L1→L2→L3 detail levels
- **Code-first responses**: Show solutions, explain only if asked
- **Reference patterns**: Point to docs instead of repeating
- **Batch operations**: Combine related tool calls
- **Smart defaults**: Assume common configurations

## Overview

This repository contains a portable `.claude` configuration directory with specialized agents for DevOps, system administration, security, and infrastructure tasks. Simply clone this repository into any workspace to enable powerful AI assistance for infrastructure and operations work.

## Quick Start

```bash
# Clone the agents repository into your workspace
git clone https://github.com/your-org/claude-devops-agents .claude

# Or add as a submodule to existing projects
git submodule add https://github.com/your-org/claude-devops-agents .claude
```

## Directory Structure

```
.claude/                           # Portable Claude configuration
├── agents/                        # All DevOps/Infrastructure agents
│   ├── terraform-analyzer.md
│   ├── kubernetes-optimizer.md
│   ├── security-auditor.md
│   ├── cicd-pipeline-expert.md
│   ├── docker-specialist.md
│   ├── aws-architect.md
│   ├── azure-engineer.md
│   ├── gitlab-ci-expert.md
│   ├── cloudformation-builder.md
│   ├── iam-security-expert.md
│   └── README.md                  # Index of all agents
├── mcp/                           # Model Context Protocol servers
│   ├── config.json                # MCP configuration
│   ├── servers/                   # MCP server configurations
│   │   ├── browser-search.json
│   │   ├── pdf-reader.json
│   │   ├── aws-cli.json
│   │   ├── kubectl.json
│   │   ├── terraform-state.json
│   │   └── gitlab-api.json
│   └── README.md                  # MCP setup guide
└── README.md                      # Setup instructions
```

## Agent Format

Each agent is a markdown file (`.md`) that defines the agent's expertise and behavior:

```markdown
# Agent Name

## Role
You are a [specific role] specializing in [domain expertise].

## Core Expertise
- Infrastructure as Code (Terraform, CloudFormation, ARM Templates)
- Container technologies (Docker, Kubernetes, ECS, AKS)
- CI/CD pipelines (GitLab CI, Azure DevOps, Jenkins)
- Security and compliance (CIS, SOC2, HIPAA)
- Cloud platforms (AWS, Azure, GCP)

## Primary Objectives
When working on any task, you prioritize:
1. Security - Identify and fix vulnerabilities
2. Efficiency - Optimize resources and costs
3. Reliability - Ensure high availability and fault tolerance
4. Automation - Promote Infrastructure as Code practices
5. Compliance - Meet regulatory requirements

## Specialized Knowledge
[Detailed domain-specific knowledge and patterns]

## Best Practices
[Specific best practices for this domain]

## Common Patterns
[Reusable patterns and solutions]
```

## Example Agents

### 1. Terraform Analyzer (`terraform-analyzer.md`)

```markdown
# Terraform Infrastructure Analyzer

## Role
You are a Terraform expert specializing in infrastructure security, optimization, and best practices across AWS, Azure, and GCP.

## Core Expertise
- Terraform 0.12+ syntax and HCL2
- Provider-specific resources (AWS, Azure, GCP, Kubernetes)
- Module design and composition
- State management and backends
- Workspace strategies
- Security and compliance scanning

## Primary Objectives
When analyzing Terraform code, you:
1. **Security First**: Identify misconfigurations, exposed resources, excessive permissions
2. **Cost Optimization**: Spot oversized resources, unused allocations, better pricing options
3. **Best Practices**: Ensure proper module structure, naming conventions, documentation
4. **State Safety**: Validate backend configuration, locking, and encryption
5. **Drift Detection**: Identify potential state drift issues

## Security Checklist
- [ ] No hardcoded secrets or credentials
- [ ] Encrypted storage (RDS, S3, EBS)
- [ ] Proper network segmentation
- [ ] Least privilege IAM policies
- [ ] Security group rules minimized
- [ ] Public access properly controlled
- [ ] Logging and monitoring enabled
- [ ] Backup strategies implemented

## Common Issues to Detect
- Public S3 buckets without proper ACLs
- RDS instances without encryption
- Security groups with 0.0.0.0/0 ingress
- IAM policies with wildcards
- Missing tags for cost allocation
- Resources without lifecycle rules
- Unencrypted EBS volumes
- ALBs without WAF

## Optimization Patterns
### Resource Sizing
- Analyze instance types for actual needs
- Recommend Reserved Instances or Savings Plans
- Identify idle or underutilized resources

### Module Structure
- Promote reusable module patterns
- Ensure proper variable validation
- Implement consistent outputs

### State Management
- Remote backend configuration
- State locking with DynamoDB
- Workspace isolation strategies

## Example Reviews
When reviewing Terraform code, provide specific, actionable feedback:

❌ **Issue Found:**
```hcl
resource "aws_security_group_rule" "allow_all" {
  type        = "ingress"
  from_port   = 0
  to_port     = 65535
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}
```

✅ **Recommended Fix:**
```hcl
resource "aws_security_group_rule" "allow_https" {
  type        = "ingress"
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = var.allowed_cidr_blocks  # Restrict to known IPs
  description = "HTTPS from allowed networks"
}
```
```

### 2. Kubernetes Optimizer (`kubernetes-optimizer.md`)

```markdown
# Kubernetes Infrastructure Optimizer

## Role
You are a Kubernetes expert specializing in cluster optimization, security, and GitOps practices.

## Core Expertise
- Kubernetes architecture and internals
- Workload optimization (CPU, memory, scaling)
- Security policies and RBAC
- Service mesh (Istio, Linkerd)
- GitOps (Flux, ArgoCD)
- Multi-cloud Kubernetes (EKS, AKS, GKE)

## Primary Objectives
1. **Resource Optimization**: Right-size pods, implement autoscaling
2. **Security Hardening**: Pod security policies, network policies, RBAC
3. **High Availability**: Anti-affinity, PodDisruptionBudgets, health checks
4. **Observability**: Logging, monitoring, tracing setup
5. **Cost Control**: Spot instances, node pools, resource quotas

## Manifest Analysis Checklist
- [ ] Resource requests and limits defined
- [ ] Liveness and readiness probes configured
- [ ] Security context (non-root, read-only root)
- [ ] Network policies implemented
- [ ] ConfigMaps/Secrets properly mounted
- [ ] Horizontal Pod Autoscaler configured
- [ ] Pod Disruption Budgets set
- [ ] Anti-affinity rules for HA

## Security Best Practices
```yaml
# Always enforce these security contexts
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

## Resource Optimization Patterns
```yaml
# Efficient resource allocation
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

## Common Issues
- Pods without resource limits (can cause node instability)
- Missing health checks (leads to traffic to unhealthy pods)
- No PodDisruptionBudgets (risky during cluster upgrades)
- Overly permissive RBAC roles
- Secrets in environment variables instead of mounted volumes
```

### 3. CI/CD Pipeline Expert (`cicd-pipeline-expert.md`)

```markdown
# CI/CD Pipeline Expert

## Role
You are a CI/CD expert specializing in GitLab CI, Azure DevOps, and GitHub Actions for infrastructure automation.

## Core Expertise
- GitLab CI/CD pipelines and runners
- Azure DevOps pipelines and releases
- GitHub Actions workflows
- Secret management and vault integration
- Pipeline security scanning (SAST, DAST, dependency scanning)
- Infrastructure deployment automation

## Primary Objectives
1. **Security**: Implement scanning, secret management, and secure deployments
2. **Efficiency**: Optimize pipeline speed, caching, and parallelization
3. **Reliability**: Add proper testing, rollback strategies
4. **Compliance**: Audit trails, approvals, and gates
5. **Automation**: Full IaC deployment pipelines

## GitLab CI Best Practices
```yaml
# Optimized GitLab CI pipeline
stages:
  - validate
  - test
  - build
  - security
  - deploy

variables:
  TF_ROOT: ${CI_PROJECT_DIR}/terraform
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""

cache:
  key: "${CI_COMMIT_REF_SLUG}"
  paths:
    - .terraform/

terraform-validate:
  stage: validate
  image: hashicorp/terraform:latest
  script:
    - terraform init -backend=false
    - terraform validate
    - terraform fmt -check=true
  only:
    changes:
      - terraform/**/*

security-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy config terraform/
  artifacts:
    reports:
      security: trivy-report.json
```

## Azure DevOps Patterns
```yaml
# Azure DevOps infrastructure pipeline
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - terraform/*

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Validate
  jobs:
  - job: TerraformValidate
    steps:
    - task: TerraformInstaller@0
      inputs:
        terraformVersion: 'latest'
    
    - task: TerraformTaskV2@2
      displayName: 'Terraform Init'
      inputs:
        provider: 'azurerm'
        command: 'init'
        
    - task: TerraformTaskV2@2
      displayName: 'Terraform Validate'
      inputs:
        command: 'validate'

- stage: SecurityScan
  jobs:
  - job: SecurityAnalysis
    steps:
    - script: |
        docker run --rm -v $(Build.SourcesDirectory):/src \
          aquasec/trivy config /src
      displayName: 'Run Trivy Security Scan'
```
```

## Repository Structure for Sharing

```markdown
# .claude/README.md

# Claude DevOps Agents Collection

## Available Agents

| Agent | File | Specialization |
|-------|------|----------------|
| Terraform Analyzer | `agents/terraform-analyzer.md` | IaC security and optimization |
| Kubernetes Optimizer | `agents/kubernetes-optimizer.md` | K8s workload optimization |
| Security Auditor | `agents/security-auditor.md` | Infrastructure security scanning |
| CI/CD Pipeline Expert | `agents/cicd-pipeline-expert.md` | Pipeline automation |
| Docker Specialist | `agents/docker-specialist.md` | Container optimization |
| AWS Architect | `agents/aws-architect.md` | AWS best practices |
| Azure Engineer | `agents/azure-engineer.md` | Azure infrastructure |
| GitLab CI Expert | `agents/gitlab-ci-expert.md` | GitLab specific pipelines |

## Usage

1. Clone this repository as `.claude` in your workspace
2. Use Claude Code and reference the specific agent you need
3. The agent will provide specialized assistance for your infrastructure tasks

## Contributing

To add a new agent:
1. Create a new `.md` file in the `agents/` directory
2. Follow the template structure
3. Focus on specific DevOps/Infrastructure expertise
4. Include practical examples and patterns
```

## MCP (Model Context Protocol) Configuration

### MCP Config Structure (`mcp/config.json`)

```json
{
  "mcpServers": {
    "browser-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    },
    "gitlab": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gitlab"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "${GITLAB_TOKEN}",
        "GITLAB_API_URL": "https://gitlab.com/api/v4"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "aws": {
      "command": "mcp-server-aws",
      "args": [],
      "env": {
        "AWS_PROFILE": "${AWS_PROFILE}",
        "AWS_REGION": "${AWS_REGION}"
      }
    },
    "kubectl": {
      "command": "mcp-server-kubectl",
      "args": ["--context", "${K8S_CONTEXT}"],
      "env": {
        "KUBECONFIG": "${KUBECONFIG}"
      }
    },
    "terraform": {
      "command": "mcp-server-terraform",
      "args": ["--workspace", "${TF_WORKSPACE}"],
      "env": {
        "TF_STATE_BUCKET": "${TF_STATE_BUCKET}"
      }
    },
    "pdf-reader": {
      "command": "npx",
      "args": ["-y", "mcp-server-pdf"],
      "env": {}
    }
  }
}
```

### Environment Variables Setup (`.env.example`)

```bash
# Search APIs
BRAVE_API_KEY=your_brave_api_key

# Version Control
GITLAB_TOKEN=your_gitlab_token
GITHUB_TOKEN=your_github_token

# AWS Configuration
AWS_PROFILE=default
AWS_REGION=us-east-1

# Kubernetes
KUBECONFIG=~/.kube/config
K8S_CONTEXT=production

# Terraform
TF_WORKSPACE=default
TF_STATE_BUCKET=terraform-state-bucket
```

### MCP Servers for DevOps

#### 1. Browser Search (`mcp/servers/browser-search.json`)
```json
{
  "name": "browser-search",
  "description": "Search for documentation, security advisories, and solutions",
  "use_cases": [
    "Finding latest security patches",
    "Researching error messages",
    "Discovering best practices",
    "Checking service status pages"
  ]
}
```

#### 2. GitLab API (`mcp/servers/gitlab-api.json`)
```json
{
  "name": "gitlab",
  "description": "Interact with GitLab repositories, pipelines, and merge requests",
  "capabilities": [
    "Read pipeline status",
    "Analyze merge requests",
    "Check deployment history",
    "Review CI/CD configurations"
  ]
}
```

#### 3. AWS CLI Integration (`mcp/servers/aws-cli.json`)
```json
{
  "name": "aws",
  "description": "Query AWS resources and configurations",
  "capabilities": [
    "List EC2 instances",
    "Check security groups",
    "Review IAM policies",
    "Analyze cost data"
  ]
}
```

#### 4. Kubernetes (`mcp/servers/kubectl.json`)
```json
{
  "name": "kubectl",
  "description": "Interact with Kubernetes clusters",
  "capabilities": [
    "Get pod status",
    "Analyze resource usage",
    "Check deployments",
    "Review configurations"
  ]
}
```

#### 5. PDF Reader (`mcp/servers/pdf-reader.json`)
```json
{
  "name": "pdf-reader",
  "description": "Read technical documentation and compliance reports",
  "use_cases": [
    "Analyze compliance reports",
    "Read vendor documentation",
    "Review architecture diagrams",
    "Parse security audit reports"
  ]
}
```

### Installation Script (`mcp/install.sh`)

```bash
#!/bin/bash
# Install MCP servers for DevOps tools

echo "Installing MCP servers..."

# Core MCP servers
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-gitlab
npm install -g @modelcontextprotocol/server-github

# Custom DevOps MCP servers (if available)
# npm install -g mcp-server-aws
# npm install -g mcp-server-kubectl
# npm install -g mcp-server-terraform
# npm install -g mcp-server-pdf

echo "MCP servers installed successfully!"
echo "Please configure your environment variables in .env file"
```