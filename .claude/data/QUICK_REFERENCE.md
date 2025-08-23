# Claude Agent Data Storage - Quick Reference

## Directory Structure
```
.claude/data/
├── agents/{agent_name}/     # Agent-specific storage
│   ├── input/               # Input files for processing
│   ├── output/              # Generated outputs
│   ├── state/               # Persistent state
│   └── cache/               # Temporary cache
├── shared/                  # Shared across agents
│   ├── templates/           # Reusable templates
│   ├── schemas/             # JSON schemas
│   ├── references/          # Reference docs
│   └── workflows/           # Workflow definitions
├── temp/                    # Temporary files (auto-cleaned)
├── archives/                # Compressed old data
├── configs/                 # Configuration backups
└── logs/                    # Execution logs
```

## Bash Commands

### Using data-manager.sh
```bash
# Initialize new agent
./data-manager.sh init my-agent

# Save output
./data-manager.sh save my-agent "output content" filename.txt

# Read input
./data-manager.sh read my-agent input-file.txt

# Update state
./data-manager.sh state my-agent '{"key": "value"}'

# List agent files
./data-manager.sh list my-agent

# Clean old files
./data-manager.sh clean 48  # Clean files older than 48 hours

# Archive outputs
./data-manager.sh archive 30  # Archive files older than 30 days

# Check disk usage
./data-manager.sh usage
```

### Direct File Operations
```bash
# Save output
echo "data" > .claude/data/agents/my-agent/output/result.txt

# Read input
cat .claude/data/agents/my-agent/input/request.txt

# Update state
echo '{"status": "ready"}' > .claude/data/agents/my-agent/state/current.json

# Use shared template
cat .claude/data/shared/templates/terraform-module.tpl
```

## Python Usage

### Basic Operations
```python
from agent_data import AgentDataManager

# Initialize
agent = AgentDataManager("my-agent")

# Save output
agent.save_output({"result": "success"}, "output.json")

# Read input
data = agent.read_input("request.json")

# Manage state
agent.set_state(status="processing", task_id="123")
state = agent.get_state()

# Use cache
agent.cache_set("results", {"data": [1, 2, 3]})
cached = agent.cache_get("results")

# List files
files = agent.list_files("output")

# Clean old files
agent.cleanup("cache", days_old=7)
```

### Workflow Management
```python
from agent_data import DataWorkflow

# Create workflow
workflow = DataWorkflow("my-workflow")

# Hand off data between agents
workflow.handoff("agent1", "agent2", {"key": "value"})

# Save workflow state
workflow.save_workflow_state()
```

## File Naming Conventions
- Use lowercase with hyphens: `cost-analysis-report.json`
- Include timestamps: `output-20250123-143022.txt`
- Be descriptive: `terraform-infrastructure-plan.yaml`

## Data Formats
- **Structured data**: JSON, YAML
- **Configurations**: TOML, INI
- **Reports**: Markdown, HTML
- **Logs**: Plain text with timestamps
- **Large data**: CSV, Parquet

## Standard JSON Structure
```json
{
  "metadata": {
    "agent": "agent-name",
    "timestamp": "2025-01-23T14:30:00Z",
    "version": "1.0.0"
  },
  "status": {
    "code": "success",
    "message": "Operation completed"
  },
  "data": {
    "your": "content here"
  }
}
```

## Environment Variables
```bash
# Set in your scripts
export CLAUDE_DATA_DIR="/mnt/e/github/agents/claude-agents/.claude/data"
export AGENT_NAME="my-agent"
export AGENT_DATA_DIR="$CLAUDE_DATA_DIR/agents/$AGENT_NAME"
```

## Common Patterns

### Agent Reading Previous Output
```bash
# Agent reads its own previous output
LAST_OUTPUT=$(ls -t .claude/data/agents/my-agent/output/*.json | head -1)
if [ -n "$LAST_OUTPUT" ]; then
    cat "$LAST_OUTPUT"
fi
```

### Cross-Agent Data Sharing
```bash
# Agent A saves output
echo "$DATA" > .claude/data/agents/agent-a/output/result.json

# Agent B reads it as input
cp .claude/data/agents/agent-a/output/result.json \
   .claude/data/agents/agent-b/input/
```

### Workflow Handoff
```json
// Handoff file structure
{
  "workflow_id": "wf-123",
  "from_agent": "terra",
  "to_agent": "k8s",
  "timestamp": "2025-01-23T14:30:00Z",
  "data": {
    "vpc_id": "vpc-123",
    "subnets": ["subnet-1", "subnet-2"]
  }
}
```

## Troubleshooting

### Permission Issues
```bash
chmod 755 .claude/data/agents/*/
chmod 644 .claude/data/agents/*/output/*
```

### Disk Space
```bash
du -sh .claude/data/*
find .claude/data -size +10M -type f
```

### Clean Stale Locks
```bash
find .claude/data/temp/processing -name "*.lock" -mmin +60 -delete
```

### Validate JSON
```bash
jq . .claude/data/agents/my-agent/state/current.json
```

## Best Practices
1. Always use absolute paths in scripts
2. Include timestamps in filenames
3. Validate JSON before saving
4. Clean cache and temp regularly
5. Archive old outputs monthly
6. Never store credentials in plain text
7. Use state files for persistence
8. Document data schemas
9. Implement proper error handling
10. Monitor disk usage