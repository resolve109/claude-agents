#!/usr/bin/env python3
"""
File Location Validator
Critical self-check mechanism to prevent saving user files in .claude directory
"""

import os
import sys
from pathlib import Path
from typing import Tuple, Optional

class FileLocationValidator:
    """Validates that files are saved in appropriate locations"""
    
    CLAUDE_DIR = '.claude'
    INTERNAL_OPERATIONS = [
        'agents',           # Agent definitions
        'scripts',          # Self-optimization scripts
        'mcp',              # MCP configurations
        'templates',        # Internal templates
        'cache',            # Internal cache
        'logs'              # Internal logs
    ]
    
    USER_FILE_LOCATIONS = {
        'terraform': '/terraform',
        'kubernetes': '/kubernetes', 
        'cloudformation': '/cloudformation',
        'docker': '/docker',
        'cicd': '/.gitlab-ci',
        'config': '/config',
        'default': '/'  # Project root
    }
    
    @staticmethod
    def is_claude_internal_path(file_path: str) -> bool:
        """Check if path is inside .claude directory"""
        return '.claude/' in file_path or file_path.startswith('.claude/')
    
    @staticmethod
    def is_internal_operation(file_path: str) -> bool:
        """Determine if this is a legitimate internal Claude operation"""
        if not FileLocationValidator.is_claude_internal_path(file_path):
            return False
            
        # Check if it's in an approved internal subdirectory
        for internal_dir in FileLocationValidator.INTERNAL_OPERATIONS:
            if f'.claude/{internal_dir}' in file_path:
                # Further validate specific file types
                if internal_dir == 'agents' and file_path.endswith('.md'):
                    return True
                elif internal_dir == 'scripts' and file_path.endswith('.py'):
                    return True
                elif internal_dir == 'mcp' and file_path.endswith('.json'):
                    return True
                elif internal_dir in ['templates', 'cache', 'logs']:
                    return True
        
        return False
    
    @staticmethod
    def get_file_type(file_path: str) -> str:
        """Determine the type of file based on extension and content"""
        ext = Path(file_path).suffix.lower()
        name = Path(file_path).stem.lower()
        
        if ext in ['.tf', '.tfvars'] or 'terraform' in name:
            return 'terraform'
        elif ext in ['.yaml', '.yml'] and any(k in name for k in ['k8s', 'kubernetes', 'deployment', 'service', 'pod']):
            return 'kubernetes'
        elif ext == '.yaml' and 'cloudformation' in name:
            return 'cloudformation'
        elif 'dockerfile' in name.lower() or ext == '.dockerfile':
            return 'docker'
        elif 'gitlab-ci' in name or 'pipeline' in name:
            return 'cicd'
        elif ext in ['.json', '.yaml', '.yml', '.ini', '.conf']:
            return 'config'
        else:
            return 'default'
    
    @staticmethod
    def suggest_proper_location(file_path: str, project_root: str = '/') -> str:
        """Suggest the proper location for a file"""
        file_name = Path(file_path).name
        file_type = FileLocationValidator.get_file_type(file_path)
        
        # Get the appropriate directory
        suggested_dir = FileLocationValidator.USER_FILE_LOCATIONS.get(file_type, '/')
        
        # Build the full path
        if suggested_dir == '/':
            return os.path.join(project_root, file_name)
        else:
            return os.path.join(project_root, suggested_dir.lstrip('/'), file_name)
    
    @staticmethod
    def validate_and_correct(file_path: str, project_root: str = None) -> Tuple[bool, Optional[str], str]:
        """
        Validate file location and suggest correction if needed
        
        Returns:
            Tuple of (is_valid, suggested_path, message)
        """
        if not project_root:
            project_root = os.getcwd()
        
        # Check if it's in .claude directory
        if FileLocationValidator.is_claude_internal_path(file_path):
            # Check if it's a legitimate internal operation
            if FileLocationValidator.is_internal_operation(file_path):
                return (True, None, "Valid internal Claude operation")
            else:
                # This is wrong! User file in .claude directory
                suggested = FileLocationValidator.suggest_proper_location(file_path, project_root)
                return (False, suggested, 
                       f"ERROR: User files cannot be saved in .claude directory!\n"
                       f"Suggested location: {suggested}")
        
        # File is outside .claude - this is good
        return (True, None, "Valid user file location")

def main():
    """CLI interface for file location validation"""
    if len(sys.argv) < 2:
        print("Usage: python file-location-validator.py <file_path> [project_root]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    project_root = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    
    validator = FileLocationValidator()
    is_valid, suggested_path, message = validator.validate_and_correct(file_path, project_root)
    
    print(f"File: {file_path}")
    print(f"Status: {'✓ VALID' if is_valid else '✗ INVALID'}")
    print(f"Message: {message}")
    
    if suggested_path:
        print(f"Suggested: {suggested_path}")
        print("\nTo fix this issue:")
        print(f"  mv {file_path} {suggested_path}")
    
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()