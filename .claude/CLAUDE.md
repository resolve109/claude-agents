# Claude Internal Configuration & Optimization Guide

## CRITICAL: File Location Architecture

### .claude Directory = Claude's Internal Operations ONLY
**THIS IS A FUNDAMENTAL RULE: The `.claude` folder is EXCLUSIVELY for Claude's internal workspace.**

#### What belongs in .claude:
- Agent definitions (`.claude/agents/*.md`)
- Self-optimization scripts (`.claude/scripts/*.py`)
- MCP configurations (`.claude/mcp/`)
- Internal references and data (`.claude/data/`)
- Claude's operational files and caches
- Agent templates and frameworks

#### What NEVER belongs in .claude:
- User task deliverables
- Project code files
- Infrastructure configurations (unless they're agent templates)
- Any files the user requests be created
- User's Terraform, Kubernetes, or Docker files
- Actual deployment configurations

### User Files = ALWAYS Outside .claude
When creating files for users:
1. **Default location**: Project root directory
2. **Organized locations**: `/terraform`, `/kubernetes`, `/cloudformation`, `/docker`, etc.
3. **User-specified**: Ask if uncertain about location
4. **NEVER**: Inside `.claude` directory

### Self-Check Protocol (MANDATORY)
```python
def validate_file_location(file_path):
    """Critical validation to prevent user files in .claude directory"""
    if '.claude/' in file_path:
        if not is_internal_claude_operation():
            raise ValueError("STOP! User files cannot be saved in .claude directory!")
            # Redirect to appropriate location
            suggested_path = file_path.replace('.claude/', '')
            return get_proper_user_file_location(suggested_path)
    return file_path  # Safe to proceed
```

## Token Optimization Strategies

### CRITICAL: Reduce Token Usage (Target: <30% of limit)

#### 1. Agent Definition Optimization
```yaml
optimization_rules:
  max_lines: 200  # Down from 500+
  format: compressed_yaml
  examples: reference_only  # Don't embed, just reference
  descriptions: use_abbreviations
  
abbreviations:
  - K8s → Kubernetes
  - TF → Terraform  
  - IaC → Infrastructure as Code
  - CICD → Continuous Integration/Deployment
  - CFN → CloudFormation
  - SG → Security Group
  - IAM → Identity Access Management
```

#### 2. Smart Data Access Patterns
```python
# Efficient data loading strategy
def load_aws_service_data(service_name):
    """Load only what's needed, when it's needed"""
    # Level 1: Check index first
    index_entry = MASTER_INDEX['services'].get(service_name)
    if not index_entry:
        return None
    
    # Level 2: Load summary only
    if needs_summary_only():
        return index_entry['summary']
    
    # Level 3: Load specific sections
    if needs_specific_section(section):
        return load_section(service_name, section)
    
    # Level 4: Full load (rare)
    return load_full_service(service_name)
```

#### 3. Response Efficiency Patterns

##### Progressive Disclosure Levels
```yaml
response_levels:
  L1_executive:
    max_tokens: 100
    content: "Key findings and critical actions only"
    
  L2_detailed:
    max_tokens: 500
    content: "Analysis, recommendations, implementation steps"
    
  L3_technical:
    max_tokens: 2000
    content: "Full code, detailed explanations, edge cases"
```

##### Code-First Responses
```python
# GOOD: Show solution immediately
def respond_with_code():
    return """
    resource "aws_s3_bucket" "secure" {
      bucket = var.bucket_name
      
      server_side_encryption_configuration {
        rule {
          apply_server_side_encryption_by_default {
            sse_algorithm = "AES256"
          }
        }
      }
    }
    # Explanation: S3 bucket with encryption enabled
    """

# BAD: Long explanation before code
def verbose_response():
    return """
    When creating an S3 bucket in AWS, it's important to consider...
    [500 words of explanation]
    ... and here's the code:
    [actual solution]
    """
```

#### 4. Batch Operations
```python
# Efficient: Single batch operation
tools.batch_read([
    "terraform/main.tf",
    "terraform/variables.tf", 
    "terraform/outputs.tf"
])

# Inefficient: Multiple individual reads
tools.read("terraform/main.tf")
tools.read("terraform/variables.tf")
tools.read("terraform/outputs.tf")
```

## Agent System Architecture

### Agent Hierarchy and Specializations
```yaml
agents:
  master:
    role: "Orchestrator and administrator"
    coordinates: ["terra", "k8s", "docker", "cicd", "aws", "secops"]
    
  terra:
    role: "Terraform infrastructure expert"
    specialties:
      - HCL syntax and modules
      - State management
      - Provider configurations
      - Cost optimization
    
  k8s:
    role: "Kubernetes optimizer"
    specialties:
      - Manifest optimization
      - Resource management
      - Security policies
      - Autoscaling
    
  docker:
    role: "Container specialist"
    specialties:
      - Dockerfile optimization
      - Multi-stage builds
      - Security scanning
      - Registry management
    
  cicd:
    role: "Pipeline automation expert"
    specialties:
      - GitLab CI
      - GitHub Actions
      - Azure DevOps
      - Jenkins
    
  aws:
    role: "AWS cloud architect"
    specialties:
      - Service selection
      - Cost optimization
      - Security best practices
      - Well-Architected Framework
    
  secops:
    role: "Security operations expert"
    specialties:
      - Vulnerability scanning
      - Compliance frameworks
      - IAM policies
      - Incident response
```

### Agent Collaboration Patterns
```python
class AgentCollaboration:
    """Defines how agents work together"""
    
    def sequential_pipeline(self, task):
        """Agents work in sequence"""
        # Terra creates infrastructure
        infra = self.terra.create_infrastructure()
        
        # Docker builds containers
        images = self.docker.build_images(infra)
        
        # K8s deploys to cluster
        deployment = self.k8s.deploy(images, infra)
        
        # SecOps validates security
        return self.secops.validate(deployment)
    
    def parallel_analysis(self, project):
        """Multiple agents analyze simultaneously"""
        results = parallel_execute([
            self.terra.analyze_terraform,
            self.k8s.analyze_manifests,
            self.docker.scan_images,
            self.secops.security_audit
        ])
        return self.master.synthesize(results)
    
    def feedback_loop(self, optimization_target):
        """Iterative optimization with feedback"""
        while not optimized:
            current = self.aws.analyze_costs()
            plan = self.terra.optimize_infrastructure(current)
            self.cicd.deploy_changes(plan)
            optimized = self.aws.validate_savings()
```

## Data Storage Structure

### AWS Service Data Organization
```
.claude/data/aws/
├── services/                  # 270+ service definitions
│   ├── compute/
│   │   ├── ec2.json          # Detailed EC2 documentation
│   │   ├── lambda.json       # Lambda functions guide
│   │   └── ecs.json          # Container service docs
│   │
│   ├── storage/
│   │   ├── s3.json           # S3 comprehensive guide
│   │   ├── ebs.json          # Block storage docs
│   │   └── efs.json          # File system docs
│   │
│   └── database/
│       ├── rds.json          # Relational database service
│       ├── dynamodb.json     # NoSQL database
│       └── aurora.json       # Aurora database
│
├── cloudformation/            # Template library
│   ├── templates/
│   │   ├── vpc-3az.yaml     # Multi-AZ VPC template
│   │   ├── ecs-cluster.yaml # ECS cluster setup
│   │   └── rds-aurora.yaml  # Aurora cluster
│   │
│   └── snippets/             # Reusable components
│       ├── security-groups.yaml
│       ├── iam-roles.yaml
│       └── parameters.yaml
│
├── config-rules/             # AWS Config compliance rules
│   ├── security/
│   │   ├── encryption-required.json
│   │   ├── public-access-blocked.json
│   │   └── mfa-enabled.json
│   │
│   └── cost/
│       ├── unused-resources.json
│       ├── oversized-instances.json
│       └── unattached-volumes.json
│
└── MASTER_INDEX.json         # Quick lookup index
```

### Master Index Structure
```json
{
  "services": {
    "ec2": {
      "category": "compute",
      "file": "services/compute/ec2.json",
      "summary": "Elastic Compute Cloud - Virtual servers",
      "pricing_model": ["on-demand", "reserved", "spot", "savings-plans"],
      "common_limits": {
        "instances_per_region": 20,
        "eips_per_region": 5
      }
    }
  },
  "templates": {
    "vpc-3az": {
      "file": "cloudformation/templates/vpc-3az.yaml",
      "description": "Multi-AZ VPC with public/private subnets",
      "parameters": ["CidrBlock", "AZCount", "EnableNatGateway"]
    }
  },
  "config_rules": {
    "s3-encryption": {
      "file": "config-rules/security/s3-encryption.json",
      "severity": "HIGH",
      "compliance": ["CIS", "NIST", "PCI-DSS"]
    }
  }
}
```

## MCP Server Configuration

### Current MCP Servers
```json
{
  "mcpServers": {
    "brave-search": {
      "purpose": "Web search for documentation and solutions",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"]
    },
    "filesystem": {
      "purpose": "File system access for project files",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/"]
    },
    "gitlab": {
      "purpose": "GitLab API integration",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gitlab"]
    },
    "github": {
      "purpose": "GitHub repository interaction",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "perplexity": {
      "purpose": "Advanced AI search",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-perplexity"]
    },
    "fetch": {
      "purpose": "HTTP/API requests",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

### MCP Usage Patterns
```python
class MCPUsageOptimizer:
    """Optimize MCP server usage for efficiency"""
    
    def search_strategy(self, query):
        """Hierarchical search strategy"""
        # Level 1: Check local cache
        if result := self.check_cache(query):
            return result
        
        # Level 2: Search internal docs
        if result := self.search_internal_docs(query):
            return result
        
        # Level 3: Use MCP search
        return self.mcp_search(query)
    
    def batch_file_operations(self, files):
        """Batch file operations through MCP"""
        # Group by operation type
        reads = [f for f in files if f.operation == 'read']
        writes = [f for f in files if f.operation == 'write']
        
        # Execute in batches
        read_results = self.mcp_filesystem.batch_read(reads)
        write_results = self.mcp_filesystem.batch_write(writes)
        
        return combine_results(read_results, write_results)
```

## Self-Optimization Capabilities

### Continuous Learning System
```python
class SelfOptimizer:
    """Claude's self-improvement system"""
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.patterns = PatternRecognizer()
        self.optimizer = ResponseOptimizer()
    
    def analyze_interaction(self, request, response):
        """Analyze each interaction for improvement"""
        # Measure efficiency
        metrics = {
            'tokens_used': count_tokens(response),
            'tools_called': count_tool_calls(response),
            'response_time': measure_time(response),
            'user_satisfaction': estimate_satisfaction(request, response)
        }
        
        # Identify patterns
        patterns = {
            'query_type': classify_query(request),
            'optimal_agent': identify_best_agent(request),
            'common_errors': find_error_patterns(response)
        }
        
        # Generate optimization
        return self.generate_optimizations(metrics, patterns)
    
    def optimize_agent_definitions(self):
        """Periodically optimize agent definitions"""
        for agent in self.list_agents():
            # Analyze usage patterns
            usage = self.analyze_agent_usage(agent)
            
            # Identify rarely used sections
            unused = find_unused_sections(agent, usage)
            
            # Compress or remove
            optimized = compress_agent_definition(agent, unused)
            
            # Save optimized version
            self.save_agent(optimized)
    
    def cache_common_responses(self):
        """Cache frequently requested information"""
        common_queries = self.identify_common_queries()
        
        for query in common_queries:
            response = self.generate_response(query)
            self.cache.store(query, response, ttl=3600)
```

### Performance Monitoring
```yaml
monitoring_metrics:
  efficiency:
    - tokens_per_response
    - tool_calls_per_task
    - cache_hit_rate
    - response_generation_time
  
  quality:
    - task_completion_rate
    - error_frequency
    - retry_rate
    - user_clarification_requests
  
  optimization:
    - agent_activation_accuracy
    - data_retrieval_efficiency
    - batch_operation_usage
    - progressive_disclosure_adoption
```

### Optimization Strategies
```python
class OptimizationStrategies:
    """Strategies for improving Claude's performance"""
    
    @staticmethod
    def compress_responses(response):
        """Compress verbose responses"""
        # Remove redundant explanations
        response = remove_redundancy(response)
        
        # Use abbreviations
        response = apply_abbreviations(response)
        
        # Compress code examples
        response = minimize_code_comments(response)
        
        return response
    
    @staticmethod
    def smart_caching():
        """Cache strategy for common requests"""
        cache_rules = {
            'aws_service_info': {'ttl': 86400},  # 24 hours
            'terraform_patterns': {'ttl': 43200},  # 12 hours
            'security_checks': {'ttl': 3600},  # 1 hour
            'cost_calculations': {'ttl': 1800}  # 30 minutes
        }
        return cache_rules
    
    @staticmethod
    def parallel_processing(tasks):
        """Process independent tasks in parallel"""
        independent = identify_independent_tasks(tasks)
        dependent = identify_dependent_tasks(tasks)
        
        # Run independent tasks in parallel
        parallel_results = parallel_execute(independent)
        
        # Run dependent tasks sequentially
        sequential_results = sequential_execute(dependent, parallel_results)
        
        return combine_results(parallel_results, sequential_results)
```

## Agent Definition Guidelines

### Template Structure
```markdown
# [Agent Name]

## Role
[Single sentence describing primary function]

## Core Expertise (Max 50 lines)
- Primary skill 1
- Primary skill 2
- Primary skill 3

## Preflight Analysis (Max 30 lines)
1. What is the user trying to achieve?
2. What resources are involved?
3. What are the risks?
4. What is the optimal approach?

## Response Strategy (Max 40 lines)
### L1: Executive Summary (2-3 sentences)
### L2: Detailed Plan (Bullet points)
### L3: Implementation (Code/commands)

## Common Patterns (Reference only)
- Pattern 1: See /data/patterns/pattern1.md
- Pattern 2: See /data/patterns/pattern2.md

## Tools & Integrations (Max 20 lines)
- Tool 1: Purpose
- Tool 2: Purpose
```

### Agent Activation Rules
```python
def select_agent(user_request):
    """Smart agent selection based on request analysis"""
    
    # Keyword-based activation
    keywords = extract_keywords(user_request)
    
    agent_keywords = {
        'terra': ['terraform', 'hcl', 'infrastructure', 'module'],
        'k8s': ['kubernetes', 'k8s', 'pod', 'deployment', 'service'],
        'docker': ['container', 'dockerfile', 'image', 'registry'],
        'cicd': ['pipeline', 'gitlab', 'github actions', 'deployment'],
        'aws': ['aws', 'ec2', 's3', 'lambda', 'cloudformation'],
        'secops': ['security', 'vulnerability', 'compliance', 'audit']
    }
    
    # Score each agent
    scores = {}
    for agent, agent_keys in agent_keywords.items():
        scores[agent] = calculate_relevance_score(keywords, agent_keys)
    
    # Return best match or master for orchestration
    if max(scores.values()) < 0.3:
        return 'master'  # No clear match, use orchestrator
    
    return max(scores, key=scores.get)
```

## Error Handling & Recovery

### Common Error Patterns
```python
error_handlers = {
    'token_limit_exceeded': {
        'detection': lambda r: len(r) > TOKEN_LIMIT,
        'recovery': 'compress_and_retry',
        'fallback': 'progressive_disclosure'
    },
    'file_not_found': {
        'detection': lambda e: 'ENOENT' in str(e),
        'recovery': 'suggest_alternative_path',
        'fallback': 'create_template'
    },
    'api_rate_limit': {
        'detection': lambda e: '429' in str(e),
        'recovery': 'exponential_backoff',
        'fallback': 'use_cached_data'
    },
    'invalid_syntax': {
        'detection': lambda e: 'SyntaxError' in str(e),
        'recovery': 'auto_fix_syntax',
        'fallback': 'provide_corrected_example'
    }
}
```

### Recovery Procedures
```python
class ErrorRecovery:
    """Automated error recovery system"""
    
    def compress_and_retry(self, response):
        """Compress response when hitting token limits"""
        # Level 1: Remove examples
        response = remove_examples(response)
        
        # Level 2: Compress code
        if still_too_large(response):
            response = compress_code(response)
        
        # Level 3: Summary only
        if still_too_large(response):
            response = generate_summary(response)
        
        return response
    
    def suggest_alternative_path(self, path):
        """Suggest alternative when file not found"""
        alternatives = [
            path.replace('.claude/', ''),
            f"terraform/{os.path.basename(path)}",
            f"kubernetes/{os.path.basename(path)}",
            f"{os.getcwd()}/{os.path.basename(path)}"
        ]
        
        for alt in alternatives:
            if os.path.exists(alt):
                return alt
        
        return create_template_path(path)
```

## Best Practices Enforcement

### Code Quality Standards
```python
quality_checks = {
    'terraform': {
        'formatting': 'terraform fmt -check',
        'validation': 'terraform validate',
        'security': 'tfsec',
        'linting': 'tflint'
    },
    'kubernetes': {
        'validation': 'kubectl --dry-run=client',
        'security': 'kubesec scan',
        'policies': 'opa test',
        'linting': 'kube-score'
    },
    'docker': {
        'security': 'trivy image',
        'linting': 'hadolint',
        'best_practices': 'dockerfile_lint'
    }
}
```

### Automated Improvements
```python
def auto_improve_code(code, language):
    """Automatically improve code quality"""
    
    improvements = []
    
    if language == 'terraform':
        # Add missing descriptions
        if 'description' not in code:
            improvements.append(add_descriptions(code))
        
        # Add validation rules
        if 'validation' not in code:
            improvements.append(add_validations(code))
        
        # Add tags
        if 'tags' not in code:
            improvements.append(add_standard_tags(code))
    
    elif language == 'kubernetes':
        # Add resource limits
        if 'limits' not in code:
            improvements.append(add_resource_limits(code))
        
        # Add security context
        if 'securityContext' not in code:
            improvements.append(add_security_context(code))
        
        # Add probes
        if 'livenessProbe' not in code:
            improvements.append(add_health_probes(code))
    
    return apply_improvements(code, improvements)
```

## Summary

This `.claude` folder represents a sophisticated, self-optimizing AI system specifically designed for DevOps and infrastructure automation. It combines:

1. **Specialized Agents**: Expert knowledge in specific domains
2. **Comprehensive Documentation**: 270+ AWS services, Config rules, and templates
3. **Token Optimization**: Aggressive strategies to minimize token usage
4. **Smart Orchestration**: Multi-agent collaboration for complex tasks
5. **Self-Improvement**: Continuous learning and optimization
6. **Error Recovery**: Robust error handling and recovery mechanisms
7. **Best Practices**: Enforcement of industry standards and security

The system is designed to be:
- **Efficient**: Minimal token usage through compression and caching
- **Intelligent**: Smart agent selection and orchestration
- **Comprehensive**: Complete AWS and DevOps coverage
- **Self-Improving**: Continuous optimization based on usage patterns
- **Reliable**: Robust error handling and recovery
- **Secure**: Security-first approach in all recommendations

Remember: The `.claude` folder is sacred space for Claude's operations. User deliverables always go outside this directory.