#!/bin/bash

# Claude Agent Data Storage Usage Examples
# This script demonstrates how agents can use the data storage system

echo "==================================="
echo "Claude Agent Data Storage Demo"
echo "==================================="
echo ""

# Set base paths
DATA_DIR="/mnt/e/github/agents/claude-agents/.claude/data"
SCRIPT_DIR="$DATA_DIR/scripts"

# 1. Initialize a new agent's data structure
echo "1. Initializing data structure for a new agent..."
$SCRIPT_DIR/data-manager.sh init demo-agent
echo ""

# 2. Save some input data for the agent
echo "2. Creating input data for demo-agent..."
cat > $DATA_DIR/agents/demo-agent/input/task-request.txt <<EOF
Task: Analyze infrastructure costs
Priority: High
Environment: Production
Requested by: DevOps Team
Date: $(date -Iseconds)
EOF
echo "Input saved to: $DATA_DIR/agents/demo-agent/input/task-request.txt"
echo ""

# 3. Simulate agent processing and saving output
echo "3. Simulating agent processing..."
OUTPUT_DATA="Analysis Complete
=================
Total Monthly Cost: \$3,456.78
Potential Savings: \$892.34
Recommendations:
- Righti-size EC2 instances
- Enable S3 lifecycle policies
- Use Reserved Instances for databases"

$SCRIPT_DIR/data-manager.sh save demo-agent "$OUTPUT_DATA" cost-analysis.txt
echo ""

# 4. Update agent state
echo "4. Updating agent state..."
STATE_JSON='{"last_analysis": "'$(date -Iseconds)'", "status": "completed", "tasks_processed": 1}'
$SCRIPT_DIR/data-manager.sh state demo-agent "$STATE_JSON"
echo ""

# 5. Create a handoff file for another agent
echo "5. Creating handoff data for next agent..."
HANDOFF_JSON='{
  "source_agent": "demo-agent",
  "target_agent": "terra",
  "timestamp": "'$(date -Iseconds)'",
  "data": {
    "action": "implement_cost_optimizations",
    "targets": ["ec2", "s3", "rds"],
    "expected_savings": 892.34
  }
}'

echo "$HANDOFF_JSON" > $DATA_DIR/agents/terra/input/optimization-request.json
echo "Handoff data saved to: $DATA_DIR/agents/terra/input/optimization-request.json"
echo ""

# 6. List data for the demo agent
echo "6. Listing all data for demo-agent..."
$SCRIPT_DIR/data-manager.sh list demo-agent
echo ""

# 7. Check disk usage
echo "7. Checking data storage disk usage..."
$SCRIPT_DIR/data-manager.sh usage
echo ""

# 8. Demonstrate Python usage
echo "8. Running Python data management example..."
python3 <<EOF
import sys
sys.path.append('$SCRIPT_DIR')
from agent_data import AgentDataManager

# Initialize manager for demo-agent
agent = AgentDataManager('demo-agent')

# List output files
print("Output files for demo-agent:")
for file_info in agent.list_files('output'):
    print(f"  - {file_info['name']} ({file_info['size']} bytes)")

# Get current state
state = agent.get_state()
print(f"\nCurrent state: {state}")

# Cache some data
agent.cache_set('analysis_results', {'cost': 3456.78, 'savings': 892.34})
cached = agent.cache_get('analysis_results')
print(f"\nCached data retrieved: {cached}")
EOF
echo ""

# 9. Show shared resources
echo "9. Listing shared resources..."
echo "Templates:"
ls -la $DATA_DIR/shared/templates/ 2>/dev/null | grep -v "^total" | tail -n +2
echo ""
echo "Schemas:"
ls -la $DATA_DIR/shared/schemas/ 2>/dev/null | grep -v "^total" | tail -n +2
echo ""

# 10. Create a workflow example
echo "10. Creating a multi-agent workflow example..."
cat > $DATA_DIR/shared/workflows/cost-optimization-workflow.json <<EOF
{
  "name": "cost-optimization",
  "version": "1.0.0",
  "description": "Multi-agent workflow for infrastructure cost optimization",
  "steps": [
    {
      "order": 1,
      "agent": "aws",
      "action": "gather_cost_data",
      "output": "cost-report.json"
    },
    {
      "order": 2,
      "agent": "terra",
      "action": "analyze_infrastructure",
      "input": "cost-report.json",
      "output": "optimization-plan.json"
    },
    {
      "order": 3,
      "agent": "cicd",
      "action": "implement_changes",
      "input": "optimization-plan.json",
      "output": "deployment-result.json"
    },
    {
      "order": 4,
      "agent": "secops",
      "action": "validate_security",
      "input": "deployment-result.json",
      "output": "security-report.json"
    }
  ],
  "on_success": "notify_team",
  "on_failure": "rollback_changes"
}
EOF
echo "Workflow saved to: $DATA_DIR/shared/workflows/cost-optimization-workflow.json"
echo ""

echo "==================================="
echo "Demo Complete!"
echo "==================================="
echo ""
echo "Summary of created files:"
echo "- Agent data directory: $DATA_DIR/agents/demo-agent/"
echo "- Input file: task-request.txt"
echo "- Output file: cost-analysis.txt"
echo "- State file: current.json"
echo "- Handoff file: $DATA_DIR/agents/terra/input/optimization-request.json"
echo "- Workflow: $DATA_DIR/shared/workflows/cost-optimization-workflow.json"
echo ""
echo "Use '$SCRIPT_DIR/data-manager.sh help' for more commands"