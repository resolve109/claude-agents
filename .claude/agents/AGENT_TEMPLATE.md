# Agent Template: [Agent Name]

## Core Identity
**Role**: [Primary role and expertise area]
**Perspective**: [How this agent views and approaches problems]
**Communication Style**: [Professional tone, level of detail, interaction approach]

## Capabilities

### Primary Functions
- [Core capability 1]
- [Core capability 2]
- [Core capability 3]

### Specialized Knowledge
- [Domain expertise area 1]
- [Domain expertise area 2]
- [Domain expertise area 3]

## Preflight Analysis Patterns

### Initial Assessment Checklist
```yaml
preflight_checks:
  - verify_prerequisites:
      - [ ] Required tools installed
      - [ ] Necessary permissions available
      - [ ] Dependencies resolved
  - environment_scan:
      - [ ] Current environment identified
      - [ ] Resource availability confirmed
      - [ ] Existing configurations backed up
  - risk_assessment:
      - [ ] Impact radius determined
      - [ ] Rollback strategy defined
      - [ ] Stakeholders identified
```

### Context Gathering Questions
1. What is the current state of [relevant system]?
2. What are the success criteria for this task?
3. Are there any constraints or deadlines?
4. What is the acceptable downtime window?
5. Who needs to be notified of changes?

## Environment Awareness

### Environment Detection
```bash
# Detect environment type
ENV_TYPE=$(cat /etc/environment | grep ENV_TYPE || echo "development")
CLUSTER_NAME=$(kubectl config current-context 2>/dev/null || echo "local")
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text 2>/dev/null)
```

### Environment-Specific Behaviors
| Environment | Validation Level | Approval Required | Rollback Strategy |
|------------|------------------|-------------------|-------------------|
| Development | Basic | None | Immediate |
| Staging | Comprehensive | Team Lead | Automated |
| Production | Exhaustive | Multi-tier | Blue-Green |

## Known Failure Patterns

### Common Issues Database
```yaml
failure_patterns:
  - pattern: "[Specific error pattern]"
    root_cause: "[Why this happens]"
    solution: "[How to fix]"
    prevention: "[How to avoid]"
    frequency: "[How often seen]"
    severity: "[Impact level]"
```

### Diagnostic Commands
```bash
# Quick diagnostics
[diagnostic_command_1]
[diagnostic_command_2]
[diagnostic_command_3]
```

## Cost Optimization Lens

### Cost Analysis Framework
```yaml
cost_factors:
  compute:
    - instance_types: [List relevant types]
    - scaling_patterns: [Auto-scaling considerations]
  storage:
    - volume_types: [Storage options]
    - retention_policies: [Data lifecycle]
  network:
    - data_transfer: [Egress costs]
    - load_balancing: [LB pricing]
  
cost_calculation: |
  Monthly Cost = (Compute Hours × Rate) + 
                 (Storage GB × Rate) + 
                 (Data Transfer GB × Rate)
```

### Optimization Recommendations
- **Quick Wins**: [Immediate cost savings]
- **Medium Term**: [1-3 month optimizations]
- **Strategic**: [Long-term architectural changes]

## Compliance Mappings

### Regulatory Requirements
| Standard | Requirement | Implementation | Validation |
|----------|------------|----------------|------------|
| SOC2 | [Requirement] | [How to implement] | [How to verify] |
| HIPAA | [Requirement] | [How to implement] | [How to verify] |
| GDPR | [Requirement] | [How to implement] | [How to verify] |
| PCI-DSS | [Requirement] | [How to implement] | [How to verify] |

### Audit Trail Requirements
```yaml
audit_requirements:
  - change_tracking: enabled
  - approval_chain: documented
  - rollback_capability: tested
  - evidence_collection: automated
```

## Tool Integration

### Required Tools
```yaml
tools:
  essential:
    - name: [tool_name]
      version: ">=X.Y.Z"
      purpose: [what it's used for]
  optional:
    - name: [tool_name]
      version: "any"
      purpose: [enhancement capability]
```

### Integration Points
- **CI/CD**: [Pipeline integration]
- **Monitoring**: [Observability tools]
- **Alerting**: [Notification systems]
- **Documentation**: [Knowledge bases]

## Safety & Recovery Procedures

### Pre-Change Backup
```bash
# Backup current state
[backup_command_1]
[backup_command_2]

# Verify backup integrity
[verification_command]
```

### Rollback Procedures
```bash
# Immediate rollback
[rollback_command_1]
[rollback_command_2]

# Verify rollback success
[verification_command]
```

### Emergency Contacts
- **On-Call**: [Contact method]
- **Escalation**: [Escalation path]
- **Vendor Support**: [Support channels]

## Response Strategy

### Progressive Disclosure Levels

#### Level 1: Executive Summary
- **What**: [One-line description]
- **Impact**: [Business impact]
- **Timeline**: [Estimated duration]
- **Risk**: [Risk level]

#### Level 2: Technical Overview
- **Approach**: [Technical strategy]
- **Components**: [Systems affected]
- **Dependencies**: [What needs coordination]
- **Validation**: [How we'll verify success]

#### Level 3: Implementation Details
- **Step-by-step**: [Detailed procedures]
- **Commands**: [Exact commands to run]
- **Checkpoints**: [Validation at each step]
- **Troubleshooting**: [Common issues and fixes]

## Validation Commands

### Pre-Implementation Validation
```bash
# Validate current state
[validation_command_1]
[validation_command_2]
```

### Post-Implementation Validation
```bash
# Confirm successful change
[validation_command_1]
[validation_command_2]

# Performance validation
[performance_check_command]

# Security validation
[security_check_command]
```

### Health Checks
```bash
# System health
[health_check_1]
[health_check_2]

# Integration health
[integration_check]
```

## Time Estimates

### Task Duration Matrix
| Task Type | Simple | Medium | Complex |
|-----------|--------|---------|---------|
| Planning | 15 min | 1 hour | 4 hours |
| Implementation | 30 min | 2 hours | 8 hours |
| Validation | 15 min | 30 min | 2 hours |
| Documentation | 10 min | 30 min | 1 hour |

### Factors Affecting Duration
- **Environment complexity**: +20% per integration
- **Change approval**: +1-2 hours for production
- **Testing requirements**: +50% for critical systems
- **Rollback planning**: +30% for high-risk changes

## Agent Collaboration Patterns

### Upstream Dependencies
```yaml
depends_on:
  - agent: [agent_name]
    for: [what they provide]
    interface: [how to communicate]
```

### Downstream Consumers
```yaml
provides_to:
  - agent: [agent_name]
    what: [what this agent provides]
    format: [output format]
```

### Collaboration Workflows
1. **Handoff Pattern**: [When to pass control]
2. **Consultation Pattern**: [When to seek input]
3. **Parallel Execution**: [What can run simultaneously]
4. **Checkpoint Sync**: [When to synchronize]

## Interaction Examples

### Example 1: [Common Scenario]
**User**: [Typical request]
**Agent Response**:
```
[Level 1 Summary]
[Level 2 Overview if needed]
[Level 3 Details if requested]
```

### Example 2: [Complex Scenario]
**User**: [Complex request]
**Agent Response**:
```
[Preflight analysis]
[Risk assessment]
[Recommended approach]
[Validation steps]
```

## Metrics & Observability

### Key Performance Indicators
- **Success Rate**: [Target percentage]
- **Mean Time to Resolution**: [Target duration]
- **Change Failure Rate**: [Acceptable threshold]
- **Recovery Time**: [Maximum acceptable]

### Monitoring Queries
```sql
-- Performance metrics
[monitoring_query_1]

-- Error tracking
[monitoring_query_2]

-- Cost tracking
[monitoring_query_3]
```

## Continuous Improvement

### Feedback Loop
- **Collection**: [How feedback is gathered]
- **Analysis**: [How patterns are identified]
- **Implementation**: [How improvements are made]
- **Validation**: [How improvements are measured]

### Knowledge Base Updates
- **Frequency**: [Update schedule]
- **Sources**: [Where new knowledge comes from]
- **Review Process**: [Quality assurance]

## Notes & Considerations

### Best Practices
- [Practice 1]
- [Practice 2]
- [Practice 3]

### Anti-Patterns to Avoid
- [Anti-pattern 1]
- [Anti-pattern 2]
- [Anti-pattern 3]

### Edge Cases
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]
- [Edge case 3]: [How to handle]