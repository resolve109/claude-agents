#!/bin/bash
# AWS Documentation Integration Helper
# Source this file to add AWS documentation functions to your environment
# Usage: source /path/to/aws-docs-integration.sh

# Base paths
export AWS_DOCS_BASE="/mnt/e/github/agents/claude-agents/.claude/data/shared/references/aws-docs"
export AWS_DOCS_SCRIPTS="/mnt/e/github/agents/claude-agents/.claude/data/scripts"

# Quick lookup function
aws-doc() {
    local cmd=$1
    shift
    
    if command -v python3 &> /dev/null; then
        python3 "$AWS_DOCS_SCRIPTS/aws-docs-lookup.py" "$cmd" "$@"
    else
        echo "Error: Python3 is required for AWS documentation lookup"
        return 1
    fi
}

# Quick service lookup
aws-service() {
    aws-doc service "$1"
}

# Quick category lookup
aws-category() {
    aws-doc category "$1"
}

# Quick search
aws-search() {
    aws-doc search "$1"
}

# Download and convert service documentation
aws-doc-get() {
    local service=$1
    if [ -z "$service" ]; then
        echo "Usage: aws-doc-get <service-name>"
        return 1
    fi
    
    python3 "$AWS_DOCS_SCRIPTS/aws-docs-converter.py" service "$service"
}

# Get PDF URL for a service
aws-doc-url() {
    local service=$1
    if [ -z "$service" ]; then
        echo "Usage: aws-doc-url <service-name>"
        return 1
    fi
    
    python3 -c "
import json
with open('$AWS_DOCS_BASE/master-index.json') as f:
    index = json.load(f)
    if '$service' in index['services']:
        print(index['services']['$service']['pdf_url'])
    else:
        print('Service not found: $service')
"
}

# List all services in a simple format
aws-services-list() {
    python3 -c "
import json
with open('$AWS_DOCS_BASE/master-index.json') as f:
    index = json.load(f)
    for service in sorted(index['services'].keys()):
        print(service)
"
}

# Get service description
aws-service-desc() {
    local service=$1
    if [ -z "$service" ]; then
        echo "Usage: aws-service-desc <service-name>"
        return 1
    fi
    
    python3 -c "
import json
with open('$AWS_DOCS_BASE/master-index.json') as f:
    index = json.load(f)
    if '$service' in index['services']:
        info = index['services']['$service']
        print(f\"{info['name']}: {info['description']}\")
    else:
        print('Service not found: $service')
"
}

# Show available commands
aws-doc-help() {
    echo "AWS Documentation Helper Functions"
    echo "==================================="
    echo ""
    echo "Available commands:"
    echo "  aws-doc <command> [args]     - Main documentation tool"
    echo "  aws-service <name>           - Get service information"
    echo "  aws-category <name>          - List services in category"
    echo "  aws-search <term>            - Search for services"
    echo "  aws-doc-get <service>        - Download and convert documentation"
    echo "  aws-doc-url <service>        - Get PDF URL for service"
    echo "  aws-services-list            - List all service keys"
    echo "  aws-service-desc <service>   - Get service description"
    echo "  aws-doc-help                 - Show this help"
    echo ""
    echo "Examples:"
    echo "  aws-service ec2"
    echo "  aws-category networking"
    echo "  aws-search lambda"
    echo "  aws-doc-get s3"
    echo "  aws-doc-url dynamodb"
}

# Export functions for use
export -f aws-doc
export -f aws-service
export -f aws-category
export -f aws-search
export -f aws-doc-get
export -f aws-doc-url
export -f aws-services-list
export -f aws-service-desc
export -f aws-doc-help

echo "AWS Documentation Integration loaded successfully!"
echo "Type 'aws-doc-help' for available commands"