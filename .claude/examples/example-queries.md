# Example Queries for DevOps Agents

## Terraform Analyzer

### Security Review
```
@terraform-analyzer Please review this Terraform code for security issues:

resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
  acl    = "public-read"
}

resource "aws_security_group" "web" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Cost Optimization
```
@terraform-analyzer How can I optimize costs for this infrastructure while maintaining high availability?
[paste your terraform code]
```

## Kubernetes Optimizer

### Pod Resource Optimization
```
@kubernetes-optimizer My pods are frequently getting OOMKilled. Here's my deployment:

apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Security Hardening
```
@kubernetes-optimizer Add security best practices to this pod spec including security context, network policies, and RBAC
```

## Docker Specialist

### Image Size Optimization
```
@docker-specialist My Docker image is 2GB. Help me optimize it. Here's my Dockerfile:

FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-pip nodejs npm
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN npm install
CMD ["python3", "app.py"]
```

### Multi-stage Build
```
@docker-specialist Convert this to a multi-stage build with security best practices for a Node.js application
```

## CI/CD Pipeline Expert

### Complete Pipeline Setup
```
@cicd-pipeline-expert Create a GitLab CI pipeline that:
1. Builds a Docker image
2. Runs security scans
3. Deploys to Kubernetes
4. Has staging and production environments
5. Requires manual approval for production
```

### Pipeline Optimization
```
@cicd-pipeline-expert My pipeline takes 45 minutes to run. How can I optimize it for speed while maintaining quality checks?
```

## Security Auditor

### Infrastructure Audit
```
@security-auditor Perform a security audit of my AWS infrastructure and check for:
- CIS AWS Foundations Benchmark compliance
- Open security groups
- Unencrypted resources
- IAM policy issues
- Public S3 buckets
```

### Incident Response
```
@security-auditor We detected suspicious activity in our Kubernetes cluster. Help me create an incident response plan and investigate.
```

## AWS Architect

### Architecture Design
```
@aws-architect Design a highly available, scalable architecture for a web application with:
- 100k daily active users
- PostgreSQL database
- Redis caching
- S3 for static assets
- Auto-scaling requirements
- Multi-region DR strategy
```

### Service Selection
```
@aws-architect Should I use ECS, EKS, or Lambda for my microservices architecture? Here are my requirements:
[list requirements]
```

## Complex Multi-Agent Scenarios

### Scenario 1: Complete Infrastructure Setup
```
I need to set up a production-ready microservices platform on AWS:

1. @aws-architect - Design the overall architecture
2. @terraform-analyzer - Create Terraform code for the infrastructure
3. @kubernetes-optimizer - Configure Kubernetes manifests
4. @security-auditor - Review everything for security
5. @gitlab-ci-expert - Create deployment pipelines
```

### Scenario 2: Migration Project
```
We're migrating from on-premise to AWS:

@aws-architect - What's the best migration strategy for our monolithic application?
@docker-specialist - How should we containerize our application?
@kubernetes-optimizer - Design the Kubernetes deployment strategy
@cicd-pipeline-expert - Set up the CI/CD pipeline for the new environment
```

### Scenario 3: Security Remediation
```
Our security scan found multiple vulnerabilities:

@security-auditor - Prioritize these vulnerabilities and create a remediation plan
@terraform-analyzer - Fix the infrastructure security issues
@docker-specialist - Harden our container images
@kubernetes-optimizer - Implement pod security policies
```

## Troubleshooting Queries

### Kubernetes Issues
```
@kubernetes-optimizer My pods are in CrashLoopBackOff. Here are the logs:
[paste logs]
```

### Pipeline Failures
```
@gitlab-ci-expert My pipeline is failing at the deploy stage with this error:
[paste error]
```

### Performance Problems
```
@aws-architect Our application is experiencing high latency. Here's our current architecture:
[describe architecture]
```

## Best Practices Queries

### Code Review Request
```
@terraform-analyzer Please review my Terraform module for:
- Security best practices
- Cost optimization
- Scalability
- Maintainability
```

### Architecture Review
```
@aws-architect Review my architecture against the Well-Architected Framework pillars
```

### Compliance Check
```
@security-auditor Ensure my infrastructure meets PCI-DSS requirements
```

## Learning and Documentation

### Educational Queries
```
@kubernetes-optimizer Explain the difference between StatefulSets and Deployments with examples
```

### Documentation Generation
```
@docker-specialist Create documentation for Docker best practices for our development team
```

### Training Material
```
@cicd-pipeline-expert Create a workshop on GitLab CI/CD best practices with hands-on exercises
```