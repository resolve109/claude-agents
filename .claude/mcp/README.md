# MCP (Model Context Protocol) Servers Configuration

## Overview

This directory contains the MCP server configuration that extends Claude's capabilities with additional tools and integrations. All servers listed in `config.json` are automatically installed and run when needed using `npx -y`.

## Available MCP Servers

### Core Tools

#### 📂 **filesystem**
- **Purpose**: Access and manipulate local files and directories
- **Usage**: Read, write, and navigate the file system
- **No API key required**

#### 🐙 **git**
- **Purpose**: Git repository operations
- **Usage**: Clone, commit, branch, and other git operations
- **No API key required**

#### 🧠 **memory**
- **Purpose**: Persistent memory across conversations
- **Usage**: Store and retrieve information between sessions
- **No API key required**

#### 🤔 **sequential-thinking**
- **Purpose**: Break down complex problems into steps
- **Usage**: Structured problem-solving approach
- **No API key required**

### Web & Browser

#### 🌐 **fetch**
- **Purpose**: Make HTTP requests to APIs and websites
- **Usage**: GET, POST, and other HTTP methods
- **No API key required**

#### 🎭 **puppeteer**
- **Purpose**: Browser automation and web scraping
- **Usage**: Navigate websites, take screenshots, extract data
- **No API key required**

#### 🔍 **web-search**
- **Purpose**: Search the web without API keys
- **Usage**: Google search results scraping
- **No API key required**

### DevOps & Cloud

#### 🐳 **docker**
- **Purpose**: Docker container management
- **Usage**: List, create, manage Docker containers and images
- **Requires**: Docker installed locally

#### ☸️ **kubernetes**
- **Purpose**: Kubernetes cluster management
- **Usage**: Deploy, scale, and manage K8s resources
- **Requires**: kubectl configured

#### ☁️ **aws-cli**
- **Purpose**: Execute AWS CLI commands
- **Usage**: Manage AWS resources via CLI
- **Requires**: AWS credentials configured

#### 📚 **aws-kb**
- **Purpose**: AWS knowledge base and best practices
- **Usage**: Query AWS documentation and patterns
- **No API key required**

### Version Control

#### 🐙 **github**
- **Purpose**: GitHub API integration
- **Usage**: Manage repos, issues, PRs
- **Requires**: `GITHUB_TOKEN` environment variable

#### 🦊 **gitlab**
- **Purpose**: GitLab API integration
- **Usage**: Manage projects, pipelines, MRs
- **Requires**: `GITLAB_TOKEN` environment variable

### Databases

#### 🗃️ **sqlite**
- **Purpose**: Local SQLite database
- **Usage**: Store and query structured data locally
- **No API key required**

#### 🐘 **postgres**
- **Purpose**: PostgreSQL database connection
- **Usage**: Query and manage PostgreSQL databases
- **Requires**: `POSTGRES_CONNECTION_STRING` environment variable

### Content Processing

#### 📺 **youtube-transcript**
- **Purpose**: Extract YouTube video transcripts
- **Usage**: Get subtitles and transcripts for analysis
- **No API key required**

#### 📝 **mdconvert**
- **Purpose**: Convert between markdown and other formats
- **Usage**: Transform documents between formats
- **No API key required**

#### ⏰ **time**
- **Purpose**: Current time and date information
- **Usage**: Get timestamps, schedule tasks
- **No API key required**

## Configuration

The `config.json` file defines all available MCP servers. Each server entry includes:

```json
{
  "server-name": {
    "command": "npx",
    "args": ["-y", "@package/name", ...additional-args],
    "env": {
      "ENV_VAR": "${ENV_VAR:-default}"
    }
  }
}
```

## Environment Variables

Create a `.env` file in your workspace root with required tokens:

```bash
# Version Control
GITHUB_TOKEN=your_github_personal_access_token
GITLAB_TOKEN=your_gitlab_personal_access_token
GITLAB_API_URL=https://gitlab.com/api/v4

# AWS
AWS_PROFILE=default
AWS_REGION=us-east-1

# Kubernetes
KUBECONFIG=~/.kube/config

# Database
POSTGRES_CONNECTION_STRING=postgresql://user:pass@localhost:5432/db
```

## How It Works

1. **Automatic Installation**: When Claude needs a tool, it automatically downloads and runs the MCP server using `npx -y`
2. **No Manual Setup**: No need to pre-install packages globally
3. **Environment Variables**: Servers read configuration from environment variables
4. **Isolated Execution**: Each server runs in its own process

## Adding New Servers

To add a new MCP server:

1. Find the server package name (usually `@org/mcp-server-name`)
2. Add entry to `config.json`:
```json
"new-server": {
  "command": "npx",
  "args": ["-y", "@org/mcp-server-name"],
  "env": {}
}
```
3. Add any required environment variables to `.env`
4. Restart Claude to load the new configuration

## Troubleshooting

### Server Not Available
- Check if the package name is correct
- Verify environment variables are set
- Ensure you have internet connection for npx to download

### Permission Errors
- Docker/Kubernetes servers need proper local permissions
- File system server needs appropriate file access

### Connection Issues
- Database servers need the service running locally/remotely
- API servers need valid tokens

## Security Notes

- **Never commit** `.env` files with real tokens
- Use **read-only tokens** when possible
- Limit file system access to specific directories
- Review server permissions before enabling

## Free vs Paid Servers

All servers in our configuration are **free to use**:
- ✅ No subscription required
- ✅ No API key costs (except for external services like GitHub/GitLab)
- ✅ Open source packages
- ✅ Run locally on your machine

Some servers require external service accounts:
- GitHub/GitLab: Free accounts work, paid for private repos
- AWS: Pay for AWS resources used, not the MCP server
- Databases: Free if running locally

## Useful MCP Server Combinations

### Web Scraping & Analysis
- `puppeteer` + `fetch` + `mdconvert`
- Scrape websites and convert content to markdown

### DevOps Workflow
- `docker` + `kubernetes` + `aws-cli`
- Complete container deployment pipeline

### Documentation Processing
- `filesystem` + `mdconvert` + `git`
- Process and version control documentation

### Database Operations
- `sqlite` + `postgres` + `filesystem`
- Data import/export and analysis

### Research & Knowledge
- `web-search` + `youtube-transcript` + `memory`
- Research topics and remember findings

## Performance Tips

1. **Selective Loading**: Only enable servers you need
2. **Token Caching**: Servers cache credentials after first use
3. **Local First**: Use local servers (sqlite, filesystem) when possible
4. **Batch Operations**: Group related operations together

## Common Issues & Solutions

### "Command not found"
- Server package name might be incorrect
- Try without the `@` prefix or check npm registry

### "Authentication failed"
- Check environment variables are set correctly
- Verify tokens haven't expired
- Ensure proper permissions on external services

### "Connection refused"
- Local services (Docker, databases) must be running
- Check firewall settings
- Verify connection strings

## Updates

MCP servers are automatically updated when using `npx -y`. To use a specific version:

```json
"server-name": {
  "command": "npx",
  "args": ["-y", "@package/name@1.2.3"],
  "env": {}
}
```

## Support

For MCP server issues:
1. Check the specific server's GitHub repository
2. Review the [MCP documentation](https://modelcontextprotocol.io)
3. Search for similar issues in the server's issue tracker

## Best Practices

1. **Start Simple**: Begin with basic servers like filesystem and git
2. **Add Gradually**: Enable additional servers as needed
3. **Monitor Usage**: Some servers may use significant resources
4. **Regular Updates**: Check for new useful MCP servers periodically
5. **Security First**: Always review what access you're granting