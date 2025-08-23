# Claude DevOps Agents Collection

A comprehensive collection of specialized AI agents for DevOps, infrastructure, and cloud engineering teams. Simply clone this `.claude` directory into any workspace to enable powerful AI assistance for infrastructure and operations work.

## 🚀 Quick Start

```bash
# Clone into your workspace as .claude directory
git clone https://github.com/your-org/claude-devops-agents .claude

# Or add as a git submodule for version control
git submodule add https://github.com/your-org/claude-devops-agents .claude
git submodule update --init --recursive
```

## 📁 Directory Structure

```
.claude/
├── agents/                    # Specialized DevOps agents
│   ├── terraform-analyzer.md  # Infrastructure as Code expert
│   ├── kubernetes-optimizer.md # K8s optimization specialist
│   ├── security-auditor.md    # Security and compliance expert
│   ├── cicd-pipeline-expert.md # CI/CD pipeline specialist
│   ├── gitlab-ci-expert.md    # GitLab CI/CD specialist
│   ├── aws-architect.md       # AWS solutions architect
│   └── docker-specialist.md   # Container optimization expert
├── mcp/                       # Model Context Protocol config
│   └── config.json           # MCP server configurations
├── templates/                 # Reusable templates
├── examples/                  # Example configurations
└── README.md                 # This file
```

## 🤖 Available Agents

### Infrastructure as Code
| Agent | Specialization | Use Cases |
|-------|---------------|-----------|
| **Terraform Analyzer** | IaC security & optimization | • Terraform code review<br>• Security vulnerability detection<br>• Cost optimization<br>• Module best practices |
| **CloudFormation Expert** | AWS native IaC | • CloudFormation templates<br>• SAM applications<br>• CDK guidance |

### Container & Orchestration
| Agent | Specialization | Use Cases |
|-------|---------------|-----------|
| **Kubernetes Optimizer** | K8s workload optimization | • Resource right-sizing<br>• Security policies<br>• High availability<br>• Cost optimization |
| **Docker Specialist** | Container optimization | • Dockerfile optimization<br>• Security scanning<br>• Multi-stage builds<br>• Registry management |
| **Helm Chart Developer** | K8s package management | • Chart development<br>• Values optimization<br>• Dependency management |

### CI/CD & Automation
| Agent | Specialization | Use Cases |
|-------|---------------|-----------|
| **CI/CD Pipeline Expert** | Multi-platform pipelines | • Pipeline optimization<br>• Security integration<br>• Multi-environment deployments |
| **GitLab CI Expert** | GitLab-specific features | • GitLab CI/CD<br>• Auto DevOps<br>• GitLab Runners |
| **GitHub Actions Expert** | GitHub workflows | • Actions workflows<br>• Reusable workflows<br>• GitHub Apps |

### Cloud Platforms
| Agent | Specialization | Use Cases |
|-------|---------------|-----------|
| **AWS Architect** | AWS solutions | • Well-Architected reviews<br>• Service selection<br>• Cost optimization<br>• Security best practices |
| **Azure Engineer** | Azure infrastructure | • ARM templates<br>• Azure DevOps<br>• AKS optimization |
| **GCP Specialist** | Google Cloud Platform | • GKE optimization<br>• Cloud Build<br>• Anthos configuration |

### Security & Compliance
| Agent | Specialization | Use Cases |
|-------|---------------|-----------|
| **Security Auditor** | Infrastructure security | • Vulnerability scanning<br>• Compliance validation<br>• Security hardening<br>• Incident response |
| **IAM Expert** | Identity management | • AWS IAM policies<br>• Azure RBAC<br>• Service accounts |

## 💡 Usage Examples

### 1. Terraform Code Review
```markdown
@terraform-analyzer Please review my Terraform code for security issues and optimization opportunities.
```

### 2. Kubernetes Troubleshooting
```markdown
@kubernetes-optimizer My pods are getting OOMKilled. Can you help me optimize resource allocation?
```

### 3. CI/CD Pipeline Creation
```markdown
@gitlab-ci-expert Create a GitLab CI pipeline for deploying a Node.js app to Kubernetes with security scanning.
```

### 4. Security Audit
```markdown
@security-auditor Perform a security audit of my AWS infrastructure and check for CIS compliance.
```

### 5. Docker Optimization
```markdown
@docker-specialist My Docker image is 2GB. Help me optimize it using multi-stage builds.
```

## 🔧 MCP (Model Context Protocol) Setup

### Available MCP Servers

The `.claude/mcp/config.json` file configures these MCP servers:

- **filesystem**: Access to local files and directories
- **browser-search**: Web search capabilities for documentation
- **gitlab**: GitLab API integration
- **github**: GitHub API integration  
- **pdf-reader**: Read technical documentation PDFs

### Environment Variables

Create a `.env` file in your workspace root:

```bash
# API Keys
BRAVE_API_KEY=your_brave_api_key

# Version Control
GITLAB_TOKEN=your_gitlab_token
GITLAB_API_URL=https://gitlab.com/api/v4
GITHUB_TOKEN=your_github_token

# Cloud Providers (optional)
AWS_PROFILE=default
AWS_REGION=us-east-1
AZURE_SUBSCRIPTION_ID=your_subscription
GCP_PROJECT_ID=your_project
```

### Installing MCP Servers

```bash
# Install MCP servers globally
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-gitlab
npm install -g @modelcontextprotocol/server-github
npm install -g mcp-server-pdf
```

## 🎯 Best Practices

### 1. Agent Selection
- Choose the most specific agent for your task
- Combine multiple agents for complex workflows
- Use general agents for exploration, specific agents for implementation

### 2. Prompt Engineering
- Be specific about your requirements
- Provide context about your environment
- Include error messages and logs when troubleshooting
- Specify any constraints (budget, compliance, performance)

### 3. Security Considerations
- Never commit sensitive data or credentials
- Use environment variables for secrets
- Review all generated code before deployment
- Run security scans on generated configurations

### 4. Version Control
- Track your `.claude` directory in git
- Use branches for experimenting with new agents
- Document custom agents and modifications
- Share improvements with the team

## 📚 Creating Custom Agents

### Agent Template

```markdown
# [Agent Name]

## Role
You are a [specific role] specializing in [domain expertise].

## Core Expertise
- List of expertise areas
- Technologies and tools
- Frameworks and methodologies

## Primary Objectives
1. **Objective 1**: Description
2. **Objective 2**: Description
3. **Objective 3**: Description

## Best Practices
[Specific best practices for this domain]

## Common Patterns
[Reusable patterns and solutions]

## Example Solutions
[Code examples and configurations]

## Troubleshooting Guide
[Common issues and solutions]

## Tools and Commands
[Relevant CLI commands and tools]
```

### Adding a New Agent

1. Create a new `.md` file in `.claude/agents/`
2. Follow the agent template structure
3. Focus on specific DevOps/Infrastructure expertise
4. Include practical examples and patterns
5. Test the agent with sample queries
6. Document in this README

## 🤝 Contributing

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Add or improve agents
4. Test your changes
5. Submit a pull request

### Contribution Guidelines

- Keep agents focused and specialized
- Include real-world examples
- Follow the existing format
- Update documentation
- Test with various scenarios

## 📈 Metrics and Monitoring

Track the effectiveness of agents:

- Response accuracy
- Time saved
- Issues resolved
- Code quality improvements
- Security vulnerabilities found

## 🔍 Troubleshooting

### Common Issues

**Agent not responding correctly:**
- Ensure the agent file is properly formatted
- Check for syntax errors in markdown
- Verify the agent is in the correct directory

**MCP servers not working:**
- Check environment variables are set
- Verify MCP servers are installed
- Review server logs for errors

**Performance issues:**
- Use specific agents instead of general ones
- Break complex tasks into smaller parts
- Cache commonly used information

## 📖 Additional Resources

### Documentation
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)

### Communities
- [DevOps Subreddit](https://www.reddit.com/r/devops/)
- [CNCF Slack](https://cloud-native.slack.com/)
- [AWS Community](https://aws.amazon.com/developer/community/)

### Training
- Cloud provider certification paths
- Kubernetes certification (CKA, CKAD, CKS)
- Security certifications (Security+, CySA+)

## 📝 License

This collection is provided as-is for use with Claude. Customize and extend based on your team's needs.

## 🆘 Support

For issues, questions, or improvements:
1. Check existing documentation
2. Search for similar issues
3. Create a detailed issue report
4. Include relevant context and examples

---

**Remember:** These agents are tools to augment your expertise, not replace it. Always review and understand generated code before using it in production.