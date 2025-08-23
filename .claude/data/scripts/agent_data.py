#!/usr/bin/env python3
"""
Claude Agent Data Management Module
Provides Python utilities for managing agent data storage
"""

import json
import os
import gzip
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import hashlib
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('agent_data')


class AgentDataManager:
    """Manager for agent-specific data storage and retrieval"""
    
    def __init__(self, agent_name: str, base_path: str = "/mnt/e/github/agents/claude-agents/.claude/data"):
        """
        Initialize data manager for a specific agent
        
        Args:
            agent_name: Name of the agent
            base_path: Base path for data storage
        """
        self.agent_name = agent_name
        self.base_path = Path(base_path)
        self.agent_path = self.base_path / "agents" / agent_name
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Initialize paths
        self.input_dir = self.agent_path / "input"
        self.output_dir = self.agent_path / "output"
        self.state_dir = self.agent_path / "state"
        self.cache_dir = self.agent_path / "cache"
        
        logger.info(f"Initialized data manager for agent: {agent_name}")
    
    def _ensure_directories(self):
        """Ensure all required directories exist"""
        for subdir in ['input', 'output', 'state', 'cache']:
            dir_path = self.agent_path / subdir
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def save_output(self, data: Any, filename: Optional[str] = None, 
                   format: str = 'json') -> Path:
        """
        Save output data for the agent
        
        Args:
            data: Data to save
            filename: Optional filename (auto-generated if not provided)
            format: Output format ('json', 'text', 'yaml')
        
        Returns:
            Path to the saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            filename = f"output-{timestamp}.{format}"
        
        output_path = self.output_dir / filename
        
        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        elif format == 'text':
            with open(output_path, 'w') as f:
                f.write(str(data))
        elif format == 'yaml':
            import yaml
            with open(output_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Saved output to: {output_path}")
        return output_path
    
    def read_input(self, filename: str) -> Any:
        """
        Read input file for the agent
        
        Args:
            filename: Name of the input file
        
        Returns:
            Content of the file (parsed if JSON/YAML, raw text otherwise)
        """
        input_path = self.input_dir / filename
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Determine format by extension
        ext = input_path.suffix.lower()
        
        if ext == '.json':
            with open(input_path, 'r') as f:
                return json.load(f)
        elif ext in ['.yaml', '.yml']:
            import yaml
            with open(input_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            with open(input_path, 'r') as f:
                return f.read()
    
    def get_state(self, key: Optional[str] = None) -> Any:
        """
        Get agent state
        
        Args:
            key: Optional specific key to retrieve
        
        Returns:
            State data or specific value if key provided
        """
        state_file = self.state_dir / "current.json"
        
        if not state_file.exists():
            return {} if key is None else None
        
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        if key:
            return state.get(key)
        return state
    
    def set_state(self, state: Dict[str, Any] = None, **kwargs):
        """
        Set agent state
        
        Args:
            state: Complete state dictionary
            **kwargs: Individual state keys to update
        """
        state_file = self.state_dir / "current.json"
        
        # Backup current state
        if state_file.exists():
            backup_file = self.state_dir / "previous.json"
            shutil.copy2(state_file, backup_file)
        
        # Load existing state or start fresh
        if state is None:
            current_state = self.get_state() or {}
            current_state.update(kwargs)
            state = current_state
        
        # Add metadata
        state['_updated'] = datetime.now().isoformat()
        state['_agent'] = self.agent_name
        
        # Save state
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2, default=str)
        
        logger.info(f"Updated state for agent: {self.agent_name}")
    
    def cache_get(self, key: str) -> Optional[Any]:
        """
        Get cached data
        
        Args:
            key: Cache key
        
        Returns:
            Cached data or None if not found/expired
        """
        cache_file = self.cache_dir / f"{key}.cache"
        
        if not cache_file.exists():
            return None
        
        # Check if cache is expired (default 7 days)
        if datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime) > timedelta(days=7):
            cache_file.unlink()
            return None
        
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    def cache_set(self, key: str, data: Any):
        """
        Set cached data
        
        Args:
            key: Cache key
            data: Data to cache
        """
        cache_file = self.cache_dir / f"{key}.cache"
        
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def list_files(self, directory: str = 'output', 
                   pattern: str = '*') -> List[Dict[str, Any]]:
        """
        List files in a directory
        
        Args:
            directory: Directory to list ('input', 'output', 'state', 'cache')
            pattern: Glob pattern for filtering
        
        Returns:
            List of file information dictionaries
        """
        dir_path = self.agent_path / directory
        
        if not dir_path.exists():
            return []
        
        files = []
        for file_path in dir_path.glob(pattern):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'name': file_path.name,
                    'path': str(file_path),
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
        
        # Sort by modified time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files
    
    def cleanup(self, directory: str = 'cache', days_old: int = 7):
        """
        Clean up old files
        
        Args:
            directory: Directory to clean
            days_old: Remove files older than this many days
        """
        dir_path = self.agent_path / directory
        
        if not dir_path.exists():
            return
        
        cutoff_time = datetime.now() - timedelta(days=days_old)
        removed_count = 0
        
        for file_path in dir_path.glob('*'):
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    file_path.unlink()
                    removed_count += 1
        
        logger.info(f"Cleaned up {removed_count} files from {directory}")
    
    def archive_outputs(self, days_old: int = 30) -> Path:
        """
        Archive old output files
        
        Args:
            days_old: Archive files older than this many days
        
        Returns:
            Path to archive file
        """
        archive_dir = self.base_path / "archives"
        archive_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        archive_path = archive_dir / f"{self.agent_name}-{timestamp}.tar.gz"
        
        cutoff_time = datetime.now() - timedelta(days=days_old)
        files_to_archive = []
        
        for file_path in self.output_dir.glob('*'):
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    files_to_archive.append(file_path)
        
        if files_to_archive:
            import tarfile
            with tarfile.open(archive_path, 'w:gz') as tar:
                for file_path in files_to_archive:
                    tar.add(file_path, arcname=file_path.name)
                    file_path.unlink()  # Remove after archiving
            
            logger.info(f"Archived {len(files_to_archive)} files to {archive_path}")
        
        return archive_path


class SharedDataManager:
    """Manager for shared data across agents"""
    
    def __init__(self, base_path: str = "/mnt/e/github/agents/claude-agents/.claude/data"):
        """
        Initialize shared data manager
        
        Args:
            base_path: Base path for data storage
        """
        self.base_path = Path(base_path)
        self.shared_path = self.base_path / "shared"
        
        # Ensure directories exist
        for subdir in ['templates', 'schemas', 'references', 'workflows']:
            (self.shared_path / subdir).mkdir(parents=True, exist_ok=True)
    
    def get_template(self, name: str) -> str:
        """Get a shared template"""
        template_path = self.shared_path / "templates" / name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {name}")
        
        with open(template_path, 'r') as f:
            return f.read()
    
    def save_workflow(self, workflow: Dict[str, Any], name: str) -> Path:
        """Save a workflow definition"""
        workflow_path = self.shared_path / "workflows" / f"{name}.json"
        
        with open(workflow_path, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        logger.info(f"Saved workflow: {name}")
        return workflow_path
    
    def get_schema(self, name: str) -> Dict[str, Any]:
        """Get a JSON schema"""
        schema_path = self.shared_path / "schemas" / name
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {name}")
        
        with open(schema_path, 'r') as f:
            return json.load(f)
    
    def validate_against_schema(self, data: Dict[str, Any], schema_name: str) -> bool:
        """
        Validate data against a schema
        
        Args:
            data: Data to validate
            schema_name: Name of the schema file
        
        Returns:
            True if valid, raises exception if invalid
        """
        import jsonschema
        
        schema = self.get_schema(schema_name)
        jsonschema.validate(data, schema)
        return True


class DataWorkflow:
    """Orchestrate data flow between agents"""
    
    def __init__(self, workflow_name: str):
        """
        Initialize workflow
        
        Args:
            workflow_name: Name of the workflow
        """
        self.workflow_name = workflow_name
        self.workflow_id = f"{workflow_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.shared_manager = SharedDataManager()
        self.agents = {}
        self.context = {
            'workflow_id': self.workflow_id,
            'started_at': datetime.now().isoformat(),
            'steps': []
        }
    
    def add_agent(self, agent_name: str) -> AgentDataManager:
        """Add an agent to the workflow"""
        if agent_name not in self.agents:
            self.agents[agent_name] = AgentDataManager(agent_name)
        return self.agents[agent_name]
    
    def handoff(self, from_agent: str, to_agent: str, 
                data: Dict[str, Any], filename: Optional[str] = None) -> Path:
        """
        Hand off data from one agent to another
        
        Args:
            from_agent: Source agent name
            to_agent: Destination agent name
            data: Data to transfer
            filename: Optional filename for the handoff
        
        Returns:
            Path to the handoff file
        """
        # Add agents if not already in workflow
        source = self.add_agent(from_agent)
        dest = self.add_agent(to_agent)
        
        # Generate handoff filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            filename = f"handoff-{from_agent}-to-{to_agent}-{timestamp}.json"
        
        # Prepare handoff data with metadata
        handoff_data = {
            'metadata': {
                'workflow_id': self.workflow_id,
                'from_agent': from_agent,
                'to_agent': to_agent,
                'timestamp': datetime.now().isoformat()
            },
            'data': data
        }
        
        # Save to destination agent's input directory
        handoff_path = dest.input_dir / filename
        with open(handoff_path, 'w') as f:
            json.dump(handoff_data, f, indent=2)
        
        # Update workflow context
        self.context['steps'].append({
            'from': from_agent,
            'to': to_agent,
            'file': str(handoff_path),
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Handoff complete: {from_agent} -> {to_agent}")
        return handoff_path
    
    def save_workflow_state(self) -> Path:
        """Save the current workflow state"""
        workflow_path = self.shared_manager.shared_path / "workflows" / f"{self.workflow_id}.json"
        
        self.context['updated_at'] = datetime.now().isoformat()
        
        with open(workflow_path, 'w') as f:
            json.dump(self.context, f, indent=2)
        
        logger.info(f"Saved workflow state: {self.workflow_id}")
        return workflow_path


# Example usage
if __name__ == "__main__":
    # Example 1: Basic agent data management
    terra = AgentDataManager("terra")
    
    # Save some output
    output_data = {
        "infrastructure": {
            "vpc_id": "vpc-123",
            "subnets": ["subnet-1", "subnet-2"]
        },
        "status": "deployed"
    }
    terra.save_output(output_data, "infrastructure-output.json")
    
    # Update state
    terra.set_state(last_deployment="2025-01-23", environment="production")
    
    # Example 2: Workflow with handoff
    workflow = DataWorkflow("infrastructure-deployment")
    
    # Terra generates infrastructure
    terra_output = {
        "vpc_id": "vpc-abc123",
        "subnet_ids": ["subnet-1", "subnet-2", "subnet-3"]
    }
    
    # Hand off to k8s agent
    workflow.handoff("terra", "k8s", terra_output)
    
    # Save workflow state
    workflow.save_workflow_state()
    
    print("Data management examples completed successfully")