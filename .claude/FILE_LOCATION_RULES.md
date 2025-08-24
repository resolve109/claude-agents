# FILE LOCATION SEPARATION RULES

## CRITICAL ARCHITECTURAL PRINCIPLE

The `.claude` directory is **EXCLUSIVELY** for Claude's internal operations and self-management. It is **NEVER** for user-requested deliverables.

## Clear Separation

### ✅ What Belongs in `.claude/`

| Directory | Purpose | File Types |
|-----------|---------|------------|
| `.claude/agents/` | Agent definitions | `*.md` files defining agent personalities |
| `.claude/scripts/` | Self-optimization scripts | `*.py` files for Claude's internal operations |
| `.claude/mcp/` | MCP server configurations | `config.json` and server definitions |
| `.claude/templates/` | Internal templates | Templates for agent creation |
| `.claude/logs/` | Internal logs | Logs from self-optimization |
| `.claude/cache/` | Internal cache | Temporary data for Claude operations |

### ❌ What NEVER Belongs in `.claude/`

| File Type | Correct Location | Example |
|-----------|-----------------|---------|
| Terraform configs | `/terraform/` or root | `main.tf`, `variables.tf` |
| Kubernetes manifests | `/kubernetes/` or `/k8s/` | `deployment.yaml`, `service.yaml` |
| CloudFormation templates | `/cloudformation/` or root | `stack.yaml`, `template.json` |
| Docker files | `/docker/` or root | `Dockerfile`, `docker-compose.yml` |
| CI/CD configs | Root or `/.gitlab-ci/` | `.gitlab-ci.yml`, `Jenkinsfile` |
| Application code | `/src/`, `/app/`, or root | `*.py`, `*.js`, `*.go` |
| Configuration files | `/config/` or root | `config.yaml`, `settings.json` |
| Documentation | `/docs/` or root | `README.md`, `*.md` |
| Any user deliverable | Project-appropriate location | Any file the user requests |

## Decision Tree

```
Is this file being created?
│
├─> Is it for Claude's internal operation?
│   │
│   ├─> YES: Is it an agent definition, self-optimization script, or MCP config?
│   │   │
│   │   ├─> YES: Save in appropriate `.claude/` subdirectory
│   │   │
│   │   └─> NO: Reconsider - probably shouldn't be in `.claude/`
│   │
│   └─> NO: This is a user deliverable
│       │
│       ├─> Does the user specify a location?
│       │   │
│       │   ├─> YES: Use the specified location
│       │   │
│       │   └─> NO: Determine based on file type
│       │       │
│       │       ├─> Infrastructure code → `/terraform/`, `/kubernetes/`, etc.
│       │       ├─> Configuration → `/config/` or root
│       │       ├─> Documentation → `/docs/` or root
│       │       └─> Default → Project root
```

## Validation Tools

### Pre-Save Validation
```python
# Use the pre-save hook for all file operations
from pre_save_hook import PreSaveHook

hook = PreSaveHook()
corrected_path, should_proceed, message = hook.intercept_save(intended_path)
```

### Manual Validation
```bash
# Validate a file path
python .claude/scripts/file-location-validator.py <file_path>

# Batch validate multiple paths
python .claude/scripts/pre-save-hook.py --batch path1,path2,path3
```

## Common Mistakes to Avoid

1. **Saving user's Terraform files in `.claude/scripts/`**
   - ❌ Wrong: `.claude/scripts/main.tf`
   - ✅ Correct: `/terraform/main.tf` or `/main.tf`

2. **Putting Kubernetes manifests in `.claude/`**
   - ❌ Wrong: `.claude/k8s-deployment.yaml`
   - ✅ Correct: `/kubernetes/deployment.yaml`

3. **Creating user documentation in `.claude/`**
   - ❌ Wrong: `.claude/PROJECT_README.md`
   - ✅ Correct: `/README.md` or `/docs/README.md`

4. **Saving configuration files in `.claude/`**
   - ❌ Wrong: `.claude/app-config.yaml`
   - ✅ Correct: `/config/app-config.yaml` or `/app-config.yaml`

## Enforcement

1. **Automatic Validation**: All file save operations should use the pre-save hook
2. **Logging**: Violations are logged to `.claude/logs/pre-save-hook.log`
3. **Correction**: Paths are automatically corrected when possible
4. **Education**: Agents learn from logged violations to improve over time

## Remember

**The `.claude` directory is Claude's workspace for self-improvement, NOT for user deliverables!**

When in doubt:
- If it's for the user → Outside `.claude/`
- If it's for Claude's internal operation → Inside `.claude/`
- If unsure → Ask the user where they want it saved