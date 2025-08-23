#!/bin/bash

# Claude Agent Data Manager
# Provides utility functions for managing agent data storage

set -e

# Configuration
DATA_BASE_DIR="/mnt/e/github/agents/claude-agents/.claude/data"
LOG_FILE="$DATA_BASE_DIR/logs/data-manager.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Logging function
log_action() {
    echo "[$(date -Iseconds)] $1" >> "$LOG_FILE"
    echo "$1"
}

# Function to save agent output
save_agent_output() {
    local agent_name=$1
    local content=$2
    local filename=${3:-"output-$(date +%Y%m%d-%H%M%S).txt"}
    
    local output_dir="$DATA_BASE_DIR/agents/$agent_name/output"
    mkdir -p "$output_dir"
    
    echo "$content" > "$output_dir/$filename"
    log_action "SAVE_OUTPUT | Agent: $agent_name | File: $filename"
    echo "Saved to: $output_dir/$filename"
}

# Function to read agent input
read_agent_input() {
    local agent_name=$1
    local filename=$2
    
    local input_file="$DATA_BASE_DIR/agents/$agent_name/input/$filename"
    
    if [ -f "$input_file" ]; then
        cat "$input_file"
        log_action "READ_INPUT | Agent: $agent_name | File: $filename"
    else
        log_action "ERROR | Agent: $agent_name | File not found: $filename"
        echo "Error: Input file not found: $input_file" >&2
        return 1
    fi
}

# Function to update agent state
update_agent_state() {
    local agent_name=$1
    local state_data=$2
    
    local state_dir="$DATA_BASE_DIR/agents/$agent_name/state"
    mkdir -p "$state_dir"
    
    local state_file="$state_dir/current.json"
    local backup_file="$state_dir/previous.json"
    
    # Backup current state if it exists
    if [ -f "$state_file" ]; then
        cp "$state_file" "$backup_file"
    fi
    
    echo "$state_data" > "$state_file"
    log_action "UPDATE_STATE | Agent: $agent_name"
}

# Function to clean temporary files
clean_temp_files() {
    local age_hours=${1:-24}
    
    log_action "CLEANUP_START | Cleaning files older than ${age_hours} hours"
    
    # Clean temp directory
    find "$DATA_BASE_DIR/temp" -type f -mmin +$((age_hours * 60)) -delete 2>/dev/null || true
    
    # Clean agent cache directories
    find "$DATA_BASE_DIR/agents/*/cache" -type f -mmin +$((age_hours * 60 * 7)) -delete 2>/dev/null || true
    
    log_action "CLEANUP_COMPLETE"
}

# Function to archive old outputs
archive_outputs() {
    local days_old=${1:-30}
    local archive_dir="$DATA_BASE_DIR/archives"
    mkdir -p "$archive_dir"
    
    local archive_name="archive-$(date +%Y%m%d).tar.gz"
    
    log_action "ARCHIVE_START | Archiving files older than ${days_old} days"
    
    # Find and archive old output files
    find "$DATA_BASE_DIR/agents/*/output" -type f -mtime +${days_old} -print0 | \
        tar -czf "$archive_dir/$archive_name" --null -T - --remove-files 2>/dev/null || true
    
    log_action "ARCHIVE_COMPLETE | Archive: $archive_name"
}

# Function to check disk usage
check_disk_usage() {
    local threshold=${1:-80}
    
    local usage=$(df "$DATA_BASE_DIR" | awk 'NR==2 {print int($5)}')
    
    if [ "$usage" -gt "$threshold" ]; then
        log_action "WARNING | Disk usage above ${threshold}%: ${usage}%"
        echo "Warning: Disk usage is ${usage}% (threshold: ${threshold}%)"
        return 1
    else
        log_action "INFO | Disk usage: ${usage}%"
        echo "Disk usage: ${usage}%"
    fi
}

# Function to list agent data
list_agent_data() {
    local agent_name=$1
    
    if [ -z "$agent_name" ]; then
        echo "Usage: list_agent_data <agent_name>"
        return 1
    fi
    
    local agent_dir="$DATA_BASE_DIR/agents/$agent_name"
    
    echo "Data for agent: $agent_name"
    echo "===================="
    
    for subdir in input output state cache; do
        local dir="$agent_dir/$subdir"
        if [ -d "$dir" ]; then
            local count=$(find "$dir" -type f | wc -l)
            local size=$(du -sh "$dir" 2>/dev/null | cut -f1)
            echo "$subdir: $count files ($size)"
            
            # List recent files
            echo "  Recent files:"
            find "$dir" -type f -printf "    %TY-%Tm-%Td %TH:%TM - %f\n" 2>/dev/null | \
                sort -r | head -5
        fi
    done
}

# Function to initialize agent data directory
init_agent_data() {
    local agent_name=$1
    
    if [ -z "$agent_name" ]; then
        echo "Usage: init_agent_data <agent_name>"
        return 1
    fi
    
    local agent_dir="$DATA_BASE_DIR/agents/$agent_name"
    
    log_action "INIT_AGENT | Creating directories for: $agent_name"
    
    mkdir -p "$agent_dir"/{input,output,state,cache}
    
    # Create initial state file
    echo '{"initialized": "'$(date -Iseconds)'", "version": "1.0.0"}' > "$agent_dir/state/init.json"
    
    echo "Initialized data directories for agent: $agent_name"
    ls -la "$agent_dir"
}

# Main command handler
case "${1:-help}" in
    save)
        save_agent_output "$2" "$3" "$4"
        ;;
    read)
        read_agent_input "$2" "$3"
        ;;
    state)
        update_agent_state "$2" "$3"
        ;;
    clean)
        clean_temp_files "$2"
        ;;
    archive)
        archive_outputs "$2"
        ;;
    usage)
        check_disk_usage "$2"
        ;;
    list)
        list_agent_data "$2"
        ;;
    init)
        init_agent_data "$2"
        ;;
    help|*)
        cat <<EOF
Claude Agent Data Manager

Usage: $0 <command> [arguments]

Commands:
  save <agent> <content> [filename]  - Save output for an agent
  read <agent> <filename>            - Read input file for an agent
  state <agent> <json_data>          - Update agent state
  clean [hours]                      - Clean temp files older than N hours (default: 24)
  archive [days]                     - Archive outputs older than N days (default: 30)
  usage [threshold]                  - Check disk usage (default threshold: 80%)
  list <agent>                       - List data files for an agent
  init <agent>                       - Initialize data directories for new agent
  help                              - Show this help message

Examples:
  $0 save terra "Infrastructure deployed successfully" deploy-log.txt
  $0 read k8s cluster-config.yaml
  $0 state cicd '{"last_build": "123", "status": "success"}'
  $0 clean 48
  $0 list terra
  $0 init new-agent

Log file: $LOG_FILE
EOF
        ;;
esac