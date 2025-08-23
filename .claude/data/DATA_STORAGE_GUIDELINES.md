# Claude Agent Data Storage Guidelines

## Directory Structure Overview

The `.claude/data/` directory serves as the centralized data storage location for all Claude agents. This structured approach ensures data isolation, easy access, and proper lifecycle management.

```
.claude/data/
├── agents/           # Agent-specific data directories
│   └── {agent_name}/
│       ├── input/    # Input files for processing
│       ├── output/   # Generated outputs and results
│       ├── state/    # Persistent state and session data
│       └── cache/    # Temporary cache files
├── shared/           # Shared resources across agents
│   ├── templates/    # Reusable templates
│   ├── schemas/      # Data schemas and models
│   ├── references/   # Reference documentation
│   └── workflows/    # Workflow definitions
├── temp/             # Temporary files (auto-cleaned)
│   ├── processing/   # Files being processed
│   ├── uploads/      # Upload staging
│   └── downloads/    # Download staging
├── archives/         # Archived data (compressed)
├── configs/          # Configuration backups
└── logs/            # Agent execution logs
```

## Best Practices

### 1. File Naming Conventions

- Use lowercase with hyphens: `infrastructure-audit-2025-01-23.json`
- Include timestamps for versioning: `state-20250123-143022.json`
- Use clear, descriptive names: `terraform-cost-analysis.txt`
- Avoid spaces and special characters

### 2. Data Organization Rules

#### Agent-Specific Data (`/agents/{agent_name}/`)
- **input/**: Raw data files that agents process
- **output/**: Results, reports, and generated files
- **state/**: Persistent state between agent runs
- **cache/**: Temporary data that can be regenerated

#### Shared Resources (`/shared/`)
- **templates/**: Reusable file templates (YAML, JSON, MD)
- **schemas/**: JSON schemas, data models
- **references/**: Lookup tables, documentation
- **workflows/**: Multi-agent workflow definitions

#### Temporary Storage (`/temp/`)
- Automatically cleaned after 24 hours
- Used for intermediate processing
- Never store critical data here

### 3. Data Lifecycle Management

#### Retention Policies
```yaml
retention_policies:
  temp:
    max_age: 24h
    auto_clean: true
  
  cache:
    max_age: 7d
    auto_clean: true
  
  output:
    max_age: 30d
    auto_archive: true
  
  state:
    max_age: unlimited
    backup: daily
  
  archives:
    max_age: 90d
    compression: gzip
```

### 4. Access Patterns

#### Reading Data
```bash
# Agent reading its own data
AGENT_DATA_DIR="/mnt/e/github/agents/claude-agents/.claude/data/agents/terra"
cat $AGENT_DATA_DIR/input/infrastructure-plan.txt

# Reading shared templates
TEMPLATE_DIR="/mnt/e/github/agents/claude-agents/.claude/data/shared/templates"
cat $TEMPLATE_DIR/terraform-module.tpl
```

#### Writing Data
```bash
# Agent writing output
OUTPUT_DIR="/mnt/e/github/agents/claude-agents/.claude/data/agents/k8s/output"
echo "Deployment successful" > $OUTPUT_DIR/deployment-$(date +%Y%m%d-%H%M%S).log

# Saving state
STATE_DIR="/mnt/e/github/agents/claude-agents/.claude/data/agents/cicd/state"
echo '{"last_run": "2025-01-23T14:30:00Z"}' > $STATE_DIR/pipeline-state.json
```

### 5. File Size Limits

- Individual files: Max 100MB
- Agent directory: Max 1GB total
- Shared directory: Max 500MB total
- Archives: Compressed, max 2GB total

### 6. Security Considerations

#### Sensitive Data
- Never store credentials in plain text
- Use `.claude/.env` for environment variables
- Encrypt sensitive files before storage
- Add sensitive patterns to `.gitignore`

#### Permissions
```bash
# Set appropriate permissions
chmod 600 .claude/data/agents/*/state/*  # State files: owner read/write only
chmod 644 .claude/data/shared/*          # Shared files: readable by all
chmod 755 .claude/data/agents/*/output/* # Output files: executable if needed
```

### 7. Data Formats

#### Preferred Formats
- **Structured Data**: JSON, YAML
- **Configurations**: TOML, INI
- **Reports**: Markdown, HTML
- **Logs**: Plain text with timestamps
- **Large Datasets**: CSV, Parquet

#### Example JSON Structure
```json
{
  "metadata": {
    "agent": "terra",
    "timestamp": "2025-01-23T14:30:00Z",
    "version": "1.0.0"
  },
  "data": {
    "key": "value"
  }
}
```

### 8. Cross-Agent Data Sharing

#### Handoff Protocol
```yaml
# Workflow output file
workflow_output:
  producer: terra
  consumer: k8s
  file: shared/workflows/infra-handoff.json
  schema: shared/schemas/infrastructure-output.json
```

#### Locking Mechanism
```bash
# Simple file-based lock
LOCK_FILE="/mnt/e/github/agents/claude-agents/.claude/data/temp/processing/terra.lock"
if [ ! -f "$LOCK_FILE" ]; then
  touch "$LOCK_FILE"
  # Process data
  rm "$LOCK_FILE"
fi
```

### 9. Backup and Recovery

#### Backup Strategy
```bash
# Daily backup of critical data
tar -czf .claude/data/archives/backup-$(date +%Y%m%d).tar.gz \
  .claude/data/agents/*/state \
  .claude/data/configs \
  .claude/data/shared
```

#### Recovery Procedure
```bash
# Restore from backup
tar -xzf .claude/data/archives/backup-20250123.tar.gz -C /
```

### 10. Monitoring and Cleanup

#### Disk Usage Monitoring
```bash
# Check data directory size
du -sh .claude/data/*
du -sh .claude/data/agents/*
```

#### Automated Cleanup
```bash
# Clean old temp files
find .claude/data/temp -type f -mtime +1 -delete

# Archive old outputs
find .claude/data/agents/*/output -type f -mtime +30 -exec gzip {} \;

# Remove old cache files
find .claude/data/agents/*/cache -type f -mtime +7 -delete
```

## Integration Examples

### Python Example
```python
import json
import os
from datetime import datetime
from pathlib import Path

class AgentDataManager:
    def __init__(self, agent_name):
        self.base_path = Path(f"/mnt/e/github/agents/claude-agents/.claude/data/agents/{agent_name}")
        self.ensure_directories()
    
    def ensure_directories(self):
        for subdir in ['input', 'output', 'state', 'cache']:
            (self.base_path / subdir).mkdir(parents=True, exist_ok=True)
    
    def save_output(self, data, filename=None):
        if filename is None:
            filename = f"output-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        output_path = self.base_path / 'output' / filename
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(output_path)
    
    def load_state(self):
        state_file = self.base_path / 'state' / 'current.json'
        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_state(self, state):
        state_file = self.base_path / 'state' / 'current.json'
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
```

### Bash Example
```bash
#!/bin/bash

# Agent data helper functions
AGENT_NAME="terra"
DATA_BASE="/mnt/e/github/agents/claude-agents/.claude/data"

save_agent_output() {
    local content="$1"
    local filename="${2:-output-$(date +%Y%m%d-%H%M%S).txt}"
    local output_path="$DATA_BASE/agents/$AGENT_NAME/output/$filename"
    
    echo "$content" > "$output_path"
    echo "Saved to: $output_path"
}

read_agent_input() {
    local filename="$1"
    local input_path="$DATA_BASE/agents/$AGENT_NAME/input/$filename"
    
    if [ -f "$input_path" ]; then
        cat "$input_path"
    else
        echo "Error: Input file not found: $input_path" >&2
        return 1
    fi
}

update_agent_state() {
    local key="$1"
    local value="$2"
    local state_file="$DATA_BASE/agents/$AGENT_NAME/state/state.json"
    
    # Create or update state
    if [ -f "$state_file" ]; then
        jq --arg k "$key" --arg v "$value" '.[$k] = $v' "$state_file" > "$state_file.tmp"
        mv "$state_file.tmp" "$state_file"
    else
        echo "{\"$key\": \"$value\"}" > "$state_file"
    fi
}
```

## Compliance and Audit

### Audit Trail
All data operations should be logged:
```bash
echo "$(date -Iseconds) | $AGENT_NAME | WRITE | $FILE_PATH" >> .claude/data/logs/data-access.log
```

### Data Governance
- Regular audits of data directories
- Compliance with retention policies
- Documentation of data lineage
- Clear ownership assignment

## Troubleshooting

### Common Issues

1. **Disk Space**: Monitor with `df -h .claude/data`
2. **Permission Errors**: Check with `ls -la .claude/data/agents/`
3. **Lock Files**: Clean stale locks in `temp/processing/`
4. **Large Files**: Compress before storing in archives
5. **Missing Directories**: Run setup script to recreate structure

### Recovery Commands
```bash
# Recreate missing directories
find .claude/data -type d | xargs mkdir -p

# Fix permissions
find .claude/data -type d -exec chmod 755 {} \;
find .claude/data -type f -exec chmod 644 {} \;

# Clean all temp files
rm -rf .claude/data/temp/*
```