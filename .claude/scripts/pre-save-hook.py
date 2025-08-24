#!/usr/bin/env python3
"""
Pre-Save Hook
Intercepts file save operations to ensure compliance with file location rules
This should be integrated into all agent workflows
"""

import os
import sys
import json
from pathlib import Path
from file_location_validator import FileLocationValidator

class PreSaveHook:
    """Pre-save validation and correction hook"""
    
    def __init__(self):
        self.validator = FileLocationValidator()
        self.log_file = Path('.claude/logs/pre-save-hook.log')
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_violation(self, original_path: str, corrected_path: str, reason: str):
        """Log location violations for analysis"""
        import datetime
        
        entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'original_path': original_path,
            'corrected_path': corrected_path,
            'reason': reason
        }
        
        # Append to log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def intercept_save(self, file_path: str, content: str = None) -> tuple:
        """
        Intercept a file save operation and validate/correct the path
        
        Args:
            file_path: Intended file path
            content: Optional file content for type detection
            
        Returns:
            (corrected_path, should_proceed, message)
        """
        project_root = os.getcwd()
        
        # Validate the intended path
        is_valid, suggested_path, message = self.validator.validate_and_correct(
            file_path, project_root
        )
        
        if is_valid:
            # Path is already correct
            return (file_path, True, "Path validated - proceeding with save")
        
        # Path needs correction
        if suggested_path:
            self.log_violation(file_path, suggested_path, message)
            
            # Create directory if needed
            suggested_dir = Path(suggested_path).parent
            suggested_dir.mkdir(parents=True, exist_ok=True)
            
            return (suggested_path, True, 
                   f"PATH CORRECTED: Redirecting from {file_path} to {suggested_path}")
        
        # Unable to determine proper location
        return (None, False, 
               f"ERROR: Cannot save to {file_path} and unable to determine proper location")
    
    def validate_batch(self, file_paths: list) -> dict:
        """Validate multiple file paths at once"""
        results = {}
        
        for file_path in file_paths:
            corrected_path, should_proceed, message = self.intercept_save(file_path)
            results[file_path] = {
                'corrected_path': corrected_path,
                'should_proceed': should_proceed,
                'message': message
            }
        
        return results

def hook_wrapper(original_save_function):
    """
    Decorator to wrap file save functions with pre-save validation
    
    Usage:
        @hook_wrapper
        def save_file(path, content):
            # original save logic
    """
    def wrapped_function(file_path, *args, **kwargs):
        hook = PreSaveHook()
        corrected_path, should_proceed, message = hook.intercept_save(file_path)
        
        print(f"[PRE-SAVE HOOK] {message}")
        
        if not should_proceed:
            raise ValueError(f"Save operation blocked: {message}")
        
        # Call original function with corrected path
        return original_save_function(corrected_path, *args, **kwargs)
    
    return wrapped_function

def main():
    """Test the pre-save hook"""
    if len(sys.argv) < 2:
        print("Usage: python pre-save-hook.py <file_path> [--batch path1,path2,...]")
        sys.exit(1)
    
    hook = PreSaveHook()
    
    if sys.argv[1] == '--batch' and len(sys.argv) > 2:
        # Batch validation
        paths = sys.argv[2].split(',')
        results = hook.validate_batch(paths)
        
        for path, result in results.items():
            print(f"\nPath: {path}")
            print(f"  Corrected: {result['corrected_path']}")
            print(f"  Proceed: {result['should_proceed']}")
            print(f"  Message: {result['message']}")
    else:
        # Single file validation
        file_path = sys.argv[1]
        corrected_path, should_proceed, message = hook.intercept_save(file_path)
        
        print(f"Original Path: {file_path}")
        print(f"Corrected Path: {corrected_path}")
        print(f"Should Proceed: {should_proceed}")
        print(f"Message: {message}")
        
        sys.exit(0 if should_proceed else 1)

if __name__ == "__main__":
    main()