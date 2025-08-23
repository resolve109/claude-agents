#!/bin/bash

# Claude DevOps Agents - Activation Script
# This script helps activate and verify the Claude agent configuration

set -e

CLAUDE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$CLAUDE_DIR/.env"
ENV_EXAMPLE="$CLAUDE_DIR/.env.example"

echo "=========================================="
echo "  Claude DevOps Agents Activation Script"
echo "=========================================="
echo ""
echo "Configuration directory: $CLAUDE_DIR"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check environment variable
check_env_var() {
    local var_name=$1
    local var_value=${!var_name}
    
    if [ -z "$var_value" ] || [[ "$var_value" == *"your_"* ]] || [[ "$var_value" == *"_here"* ]]; then
        echo "  ⚠️  $var_name: Not configured"
        return 1
    else
        # Mask the value for security
        if [ ${#var_value} -gt 8 ]; then
            local masked_value="${var_value:0:4}****${var_value: -4}"
        else
            local masked_value="****"
        fi
        echo "  ✅ $var_name: Configured ($masked_value)"
        return 0
    fi
}

# Step 1: Check for .env file
echo "Step 1: Checking environment configuration..."
echo "----------------------------------------"

if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  No .env file found"
    
    if [ -f "$ENV_EXAMPLE" ]; then
        echo "   Creating .env from template..."
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        echo "   ✅ Created .env file from template"
        echo "   ⚠️  Please edit $ENV_FILE and add your credentials"
    else
        echo "   Creating default .env file..."
        cp "$CLAUDE_DIR/.env" "$ENV_FILE"
        echo "   ✅ Created .env file"
    fi
else
    echo "✅ .env file exists"
fi

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
    echo "✅ Environment variables loaded"
fi

echo ""

# Step 2: Check prerequisites
echo "Step 2: Checking prerequisites..."
echo "----------------------------------------"

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js installed: $NODE_VERSION"
else
    echo "❌ Node.js not found - Required for MCP servers"
    echo "   Install from: https://nodejs.org/"
fi

# Check npm/npx
if command_exists npx; then
    NPX_VERSION=$(npx --version)
    echo "✅ npx installed: $NPX_VERSION"
else
    echo "❌ npx not found - Required for MCP servers"
fi

# Check Git
if command_exists git; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo "✅ Git installed: $GIT_VERSION"
else
    echo "⚠️  Git not found - Recommended for version control"
fi

# Check Docker
if command_exists docker; then
    echo "✅ Docker installed"
else
    echo "⚠️  Docker not found - Optional for container operations"
fi

# Check kubectl
if command_exists kubectl; then
    echo "✅ kubectl installed"
else
    echo "⚠️  kubectl not found - Optional for Kubernetes operations"
fi

# Check AWS CLI
if command_exists aws; then
    echo "✅ AWS CLI installed"
else
    echo "⚠️  AWS CLI not found - Optional for AWS operations"
fi

echo ""

# Step 3: Check environment variables
echo "Step 3: Checking environment variables..."
echo "----------------------------------------"

CONFIGURED_COUNT=0
TOTAL_COUNT=0

# Check critical environment variables
for var in GITHUB_TOKEN GITLAB_TOKEN POSTGRES_CONNECTION_STRING AWS_PROFILE AWS_REGION KUBECONFIG; do
    ((TOTAL_COUNT++))
    if check_env_var "$var"; then
        ((CONFIGURED_COUNT++))
    fi
done

# Handle case where no variables are properly set
if [ "$TOTAL_COUNT" -eq 0 ]; then
    echo "  ⚠️  No environment variables checked"
fi

echo ""
echo "Environment variables: $CONFIGURED_COUNT/$TOTAL_COUNT configured"

echo ""

# Step 4: Test MCP servers
echo "Step 4: Testing MCP server availability..."
echo "----------------------------------------"

# Test a basic MCP server that doesn't need configuration
echo -n "Testing filesystem MCP server... "
if npx -y @modelcontextprotocol/server-filesystem --help >/dev/null 2>&1; then
    echo "✅ Working"
else
    echo "⚠️  Not available (will download on first use)"
fi

echo ""

# Step 5: Summary
echo "=========================================="
echo "  Activation Summary"
echo "=========================================="
echo ""

# Count MCP servers
MCP_COUNT=$(grep -c '"command"' "$CLAUDE_DIR/mcp/config.json" 2>/dev/null || echo "0")
echo "📊 MCP Servers configured: $MCP_COUNT"

# Count agents
AGENT_COUNT=$(ls -1 "$CLAUDE_DIR/agents/"*.md 2>/dev/null | wc -l)
echo "🤖 Agents available: $AGENT_COUNT"

echo ""

# Determine overall status
if [ "$CONFIGURED_COUNT" -eq 0 ]; then
    echo "🟡 Status: PARTIALLY READY"
    echo ""
    echo "Basic functionality is available. To enable full capabilities:"
    echo "1. Edit $ENV_FILE"
    echo "2. Add your API tokens and credentials"
    echo "3. Run this script again to verify"
else
    echo "🟢 Status: READY"
    echo ""
    echo "Your Claude DevOps agents are activated and ready to use!"
fi

echo ""
echo "📚 Documentation: $CLAUDE_DIR/ACTIVATION_STATUS.md"
echo ""

# Step 6: Quick test commands
echo "Quick Test Commands:"
echo "----------------------------------------"
echo "# Test filesystem MCP server:"
echo "  npx -y @modelcontextprotocol/server-filesystem /"
echo ""
echo "# Load environment variables in your shell:"
echo "  source $ENV_FILE"
echo ""
echo "# View all agents:"
echo "  ls -la $CLAUDE_DIR/agents/"
echo ""

exit 0