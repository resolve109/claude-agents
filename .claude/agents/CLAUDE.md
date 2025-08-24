---
name: CLAUDE
description: Agent for CLAUDE operations
model: inherit
color: blue
---

# Claude DevOps Agents

## File Location Rules
**.claude folder** = Claude internal ONLY (agents, configs, MCP)
**User files** = ALWAYS outside .claude (project root, /terraform, /kubernetes, etc)

Before saving: If path contains `.claude/` → Only for internal ops, else redirect outside

## Structure
`.claude/agents/` - Agent definitions
`.claude/mcp/` - MCP configs

## Agent Format
Role → Expertise → Objectives → Knowledge → Patterns

## Agents
master, terra, k8s, cicd, secops, aws, docker, nginx, redis, compliance, docs
See individual files for details.

## Usage
Clone as `.claude` in workspace. Agents auto-load.

## MCP Configuration
See `mcp/config.json` for server configs (browser-search, filesystem, gitlab, github, aws, kubectl, terraform, pdf-reader).

### Env Vars
BRAVE_API_KEY, GITLAB_TOKEN, GITHUB_TOKEN, AWS_PROFILE, AWS_REGION, KUBECONFIG, K8S_CONTEXT, TF_WORKSPACE, TF_STATE_BUCKET

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