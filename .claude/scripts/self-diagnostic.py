#!/usr/bin/env python3
"""
Self-Diagnostic System for Claude Ecosystem
Comprehensive system analysis, self-correction, and auto-optimization
"""

import os
import sys
import json
import yaml
import subprocess
import platform
from pathlib import Path
from datetime import datetime
import hashlib
import shutil

class SelfDiagnosticSystem:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.diagnostic_log = self.base_path / "data" / "diagnostic_log.json"
        self.system_state = self.base_path / "data" / "system_state.json"
        
        # Diagnostic categories
        self.diagnostic_categories = {
            'structure': self.check_folder_structure,
            'agents': self.check_agents,
            'configuration': self.check_configuration,
            'dependencies': self.check_dependencies,
            'permissions': self.check_permissions,
            'performance': self.check_performance,
            'security': self.check_security,
            'integrity': self.check_integrity
        }
        
        # Auto-fix mappings
        self.auto_fixes = {
            'missing_folder': self.fix_missing_folder,
            'missing_file': self.fix_missing_file,
            'invalid_config': self.fix_invalid_config,
            'permission_issue': self.fix_permissions,
            'broken_agent': self.fix_broken_agent,
            'missing_dependency': self.fix_missing_dependency
        }
        
        self.issues_found = []
        self.fixes_applied = []
    
    def run_full_diagnostic(self, auto_fix=True):
        """Run complete system diagnostic"""
        print("🔬 CLAUDE ECOSYSTEM SELF-DIAGNOSTIC")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Auto-fix: {'ENABLED' if auto_fix else 'DISABLED'}")
        print("=" * 60)
        
        diagnostic_results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self.get_system_info(),
            'checks': {},
            'issues': [],
            'fixes_applied': [],
            'overall_health': 'unknown'
        }
        
        # Run all diagnostic checks
        for category, check_func in self.diagnostic_categories.items():
            print(f"\n🔍 Checking {category.upper()}...")
            result = check_func()
            diagnostic_results['checks'][category] = result
            
            # Display results
            if result['status'] == 'healthy':
                print(f"  ✅ {category.title()}: HEALTHY")
            elif result['status'] == 'warning':
                print(f"  ⚠️  {category.title()}: WARNING")
                for issue in result.get('issues', []):
                    print(f"     - {issue}")
            else:
                print(f"  ❌ {category.title()}: CRITICAL")
                for issue in result.get('issues', []):
                    print(f"     - {issue}")
        
        # Collect all issues
        for category, result in diagnostic_results['checks'].items():
            if 'issues' in result:
                for issue in result['issues']:
                    diagnostic_results['issues'].append({
                        'category': category,
                        'issue': issue,
                        'severity': result['status']
                    })
        
        # Apply auto-fixes if enabled
        if auto_fix and diagnostic_results['issues']:
            print("\n🔧 APPLYING AUTO-FIXES...")
            self.apply_auto_fixes(diagnostic_results)
            diagnostic_results['fixes_applied'] = self.fixes_applied
        
        # Calculate overall health
        diagnostic_results['overall_health'] = self.calculate_overall_health(diagnostic_results)
        
        # Save diagnostic results
        self.save_diagnostic_results(diagnostic_results)
        
        # Display summary
        self.display_summary(diagnostic_results)
        
        return diagnostic_results
    
    def get_system_info(self):
        """Gather system information"""
        return {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'working_directory': str(self.base_path),
            'user': os.environ.get('USER', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }
    
    def check_folder_structure(self):
        """Check if all required folders exist"""
        result = {'status': 'healthy', 'issues': []}
        
        required_folders = [
            'agents',
            'data',
            'data/backups',
            'data/aws-docs',
            'examples',
            'mcp',
            'scripts',
            'templates'
        ]
        
        for folder in required_folders:
            folder_path = self.base_path / folder
            if not folder_path.exists():
                result['status'] = 'critical'
                result['issues'].append(f"Missing folder: {folder}")
                self.issues_found.append(('missing_folder', folder))
        
        return result
    
    def check_agents(self):
        """Check agent files and configurations"""
        result = {'status': 'healthy', 'issues': []}
        agents_path = self.base_path / "agents"
        
        if not agents_path.exists():
            result['status'] = 'critical'
            result['issues'].append("Agents folder missing")
            return result
        
        # Check for essential agents
        essential_agents = ['master.md', 'orchestrator.md']
        for agent in essential_agents:
            agent_path = agents_path / agent
            if not agent_path.exists():
                result['status'] = 'critical'
                result['issues'].append(f"Essential agent missing: {agent}")
                self.issues_found.append(('missing_file', f"agents/{agent}"))
        
        # Check agent configurations
        for agent_file in agents_path.glob("*.md"):
            if agent_file.name == "AGENT_TEMPLATE.md":
                continue
                
            try:
                with open(agent_file, 'r') as f:
                    content = f.read()
                    
                # Check for valid frontmatter
                if not content.startswith('---'):
                    result['status'] = 'warning'
                    result['issues'].append(f"Invalid configuration: {agent_file.name}")
                    self.issues_found.append(('broken_agent', agent_file.name))
                    
            except Exception as e:
                result['status'] = 'warning'
                result['issues'].append(f"Cannot read agent: {agent_file.name}")
        
        return result
    
    def check_configuration(self):
        """Check configuration files"""
        result = {'status': 'healthy', 'issues': []}
        
        # Check .env file
        env_file = self.base_path / ".env"
        if not env_file.exists():
            result['status'] = 'warning'
            result['issues'].append("Environment file (.env) missing")
            self.issues_found.append(('missing_file', '.env'))
        
        # Check MCP configuration
        mcp_config = self.base_path / "mcp" / "config.json"
        if mcp_config.exists():
            try:
                with open(mcp_config, 'r') as f:
                    config = json.load(f)
                    if not isinstance(config, dict):
                        result['status'] = 'warning'
                        result['issues'].append("Invalid MCP configuration format")
                        self.issues_found.append(('invalid_config', 'mcp/config.json'))
            except json.JSONDecodeError:
                result['status'] = 'critical'
                result['issues'].append("MCP configuration is not valid JSON")
                self.issues_found.append(('invalid_config', 'mcp/config.json'))
        
        return result
    
    def check_dependencies(self):
        """Check system dependencies"""
        result = {'status': 'healthy', 'issues': []}
        
        # Check for Python modules
        required_modules = ['json', 'yaml', 'pathlib', 'datetime']
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                result['status'] = 'warning'
                result['issues'].append(f"Missing Python module: {module}")
                self.issues_found.append(('missing_dependency', module))
        
        # Check for external tools (optional)
        optional_tools = ['git', 'docker', 'kubectl']
        for tool in optional_tools:
            if shutil.which(tool) is None:
                # Just note it, don't mark as issue
                pass
        
        return result
    
    def check_permissions(self):
        """Check file and folder permissions"""
        result = {'status': 'healthy', 'issues': []}
        
        # Check write permissions on key directories
        writable_dirs = ['data', 'agents', 'scripts']
        for dir_name in writable_dirs:
            dir_path = self.base_path / dir_name
            if dir_path.exists() and not os.access(dir_path, os.W_OK):
                result['status'] = 'critical'
                result['issues'].append(f"No write permission: {dir_name}")
                self.issues_found.append(('permission_issue', dir_name))
        
        # Check execute permissions on scripts
        scripts_dir = self.base_path / "scripts"
        if scripts_dir.exists():
            for script in scripts_dir.glob("*.py"):
                if not os.access(script, os.X_OK):
                    # Python scripts don't need execute permission
                    pass
        
        return result
    
    def check_performance(self):
        """Check system performance metrics"""
        result = {'status': 'healthy', 'issues': []}
        
        # Check disk space
        stat = os.statvfs(self.base_path)
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        
        if free_gb < 1:
            result['status'] = 'critical'
            result['issues'].append(f"Low disk space: {free_gb:.2f} GB free")
        elif free_gb < 5:
            result['status'] = 'warning'
            result['issues'].append(f"Disk space warning: {free_gb:.2f} GB free")
        
        # Check for large log files
        data_dir = self.base_path / "data"
        if data_dir.exists():
            for file in data_dir.rglob("*.json"):
                size_mb = file.stat().st_size / (1024**2)
                if size_mb > 100:
                    result['status'] = 'warning'
                    result['issues'].append(f"Large file: {file.name} ({size_mb:.1f} MB)")
        
        return result
    
    def check_security(self):
        """Check security settings"""
        result = {'status': 'healthy', 'issues': []}
        
        # Check for exposed sensitive files
        env_file = self.base_path / ".env"
        if env_file.exists():
            # Check if .env is in gitignore
            gitignore = self.base_path.parent / ".gitignore"
            if gitignore.exists():
                with open(gitignore, 'r') as f:
                    if '.env' not in f.read() and '.claude/.env' not in f.read():
                        result['status'] = 'critical'
                        result['issues'].append(".env file not in .gitignore")
        
        # Check for default/weak configurations
        # This is a placeholder for more sophisticated checks
        
        return result
    
    def check_integrity(self):
        """Check system integrity"""
        result = {'status': 'healthy', 'issues': []}
        
        # Verify critical files haven't been corrupted
        critical_files = [
            'agents/master.md',
            'agents/orchestrator.md'
        ]
        
        for file_path in critical_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        content = f.read()
                        if len(content) < 100:  # Suspiciously small
                            result['status'] = 'warning'
                            result['issues'].append(f"Possibly corrupted file: {file_path}")
                except:
                    result['status'] = 'warning'
                    result['issues'].append(f"Cannot verify integrity: {file_path}")
        
        return result
    
    def apply_auto_fixes(self, diagnostic_results):
        """Apply automatic fixes for detected issues"""
        for issue_type, issue_detail in self.issues_found:
            if issue_type in self.auto_fixes:
                fix_func = self.auto_fixes[issue_type]
                try:
                    success, message = fix_func(issue_detail)
                    if success:
                        print(f"  ✅ Fixed: {message}")
                        self.fixes_applied.append(message)
                    else:
                        print(f"  ❌ Failed to fix: {message}")
                except Exception as e:
                    print(f"  ❌ Error fixing {issue_type}: {e}")
    
    def fix_missing_folder(self, folder_name):
        """Create missing folder"""
        folder_path = self.base_path / folder_name
        try:
            folder_path.mkdir(parents=True, exist_ok=True)
            return True, f"Created missing folder: {folder_name}"
        except Exception as e:
            return False, f"Could not create folder {folder_name}: {e}"
    
    def fix_missing_file(self, file_path):
        """Create missing file with appropriate template"""
        full_path = self.base_path / file_path
        
        try:
            if file_path == '.env':
                # Create from template if exists
                template = self.base_path / ".env.template"
                if template.exists():
                    shutil.copy(template, full_path)
                else:
                    # Create basic .env
                    with open(full_path, 'w') as f:
                        f.write("# Claude Environment Variables\n")
                        f.write("CLAUDE_ENV=production\n")
                return True, f"Created {file_path} from template"
                
            elif file_path.startswith('agents/'):
                # Create basic agent file
                agent_name = Path(file_path).stem
                content = f"""---
name: {agent_name}
description: Auto-generated agent for {agent_name} operations
model: inherit
color: blue
---

# {agent_name.upper()} Agent

Auto-generated by self-diagnostic system.
"""
                full_path.parent.mkdir(exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)
                return True, f"Created agent file: {file_path}"
            
            else:
                # Create empty file
                full_path.parent.mkdir(exist_ok=True)
                full_path.touch()
                return True, f"Created empty file: {file_path}"
                
        except Exception as e:
            return False, f"Could not create {file_path}: {e}"
    
    def fix_invalid_config(self, config_path):
        """Fix invalid configuration files"""
        full_path = self.base_path / config_path
        
        try:
            if config_path == 'mcp/config.json':
                # Create basic valid MCP config
                basic_config = {
                    "mcpServers": {},
                    "version": "1.0.0"
                }
                with open(full_path, 'w') as f:
                    json.dump(basic_config, f, indent=2)
                return True, f"Reset {config_path} to valid configuration"
            else:
                return False, f"No fix available for {config_path}"
        except Exception as e:
            return False, f"Could not fix {config_path}: {e}"
    
    def fix_permissions(self, path):
        """Fix permission issues"""
        full_path = self.base_path / path
        
        try:
            # Set appropriate permissions
            if full_path.is_dir():
                os.chmod(full_path, 0o755)
            else:
                os.chmod(full_path, 0o644)
            return True, f"Fixed permissions for {path}"
        except Exception as e:
            return False, f"Could not fix permissions for {path}: {e}"
    
    def fix_broken_agent(self, agent_name):
        """Fix broken agent configuration"""
        agent_path = self.base_path / "agents" / agent_name
        
        try:
            with open(agent_path, 'r') as f:
                content = f.read()
            
            # Add missing frontmatter
            if not content.startswith('---'):
                name = agent_name.replace('.md', '')
                frontmatter = f"""---
name: {name}
description: Agent for {name} operations
model: inherit
color: blue
---

"""
                content = frontmatter + content
                
                # Backup original
                backup_path = self.base_path / "data" / "backups" / f"{agent_name}.backup"
                backup_path.parent.mkdir(exist_ok=True)
                shutil.copy(agent_path, backup_path)
                
                # Write fixed content
                with open(agent_path, 'w') as f:
                    f.write(content)
                
                return True, f"Fixed configuration for {agent_name}"
            
            return False, f"No fix needed for {agent_name}"
            
        except Exception as e:
            return False, f"Could not fix {agent_name}: {e}"
    
    def fix_missing_dependency(self, dependency):
        """Attempt to install missing dependency"""
        try:
            if dependency in ['yaml', 'pyyaml']:
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyyaml'], 
                             check=True, capture_output=True)
                return True, f"Installed missing module: {dependency}"
            else:
                return False, f"Cannot auto-install {dependency}"
        except:
            return False, f"Failed to install {dependency}"
    
    def calculate_overall_health(self, diagnostic_results):
        """Calculate overall system health"""
        critical_count = sum(1 for check in diagnostic_results['checks'].values() 
                           if check['status'] == 'critical')
        warning_count = sum(1 for check in diagnostic_results['checks'].values() 
                          if check['status'] == 'warning')
        
        if critical_count > 0:
            return 'critical'
        elif warning_count > 2:
            return 'warning'
        else:
            return 'healthy'
    
    def save_diagnostic_results(self, results):
        """Save diagnostic results to file"""
        # Save current results
        self.diagnostic_log.parent.mkdir(exist_ok=True)
        
        # Load existing log or create new
        if self.diagnostic_log.exists():
            with open(self.diagnostic_log, 'r') as f:
                log = json.load(f)
        else:
            log = {'diagnostics': []}
        
        log['diagnostics'].append(results)
        
        # Keep only last 20 diagnostics
        if len(log['diagnostics']) > 20:
            log['diagnostics'] = log['diagnostics'][-20:]
        
        with open(self.diagnostic_log, 'w') as f:
            json.dump(log, f, indent=2)
        
        # Also save current system state
        with open(self.system_state, 'w') as f:
            json.dump(results, f, indent=2)
    
    def display_summary(self, diagnostic_results):
        """Display diagnostic summary"""
        print("\n" + "=" * 60)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 60)
        
        # Overall health
        health = diagnostic_results['overall_health']
        health_icons = {
            'healthy': '✅',
            'warning': '⚠️',
            'critical': '❌'
        }
        
        print(f"\nOVERALL SYSTEM HEALTH: {health_icons.get(health, '❓')} {health.upper()}")
        
        # Issue count
        print(f"\nIssues Found: {len(diagnostic_results['issues'])}")
        if diagnostic_results['issues']:
            # Group by severity
            critical = [i for i in diagnostic_results['issues'] if i['severity'] == 'critical']
            warning = [i for i in diagnostic_results['issues'] if i['severity'] == 'warning']
            
            if critical:
                print(f"  ❌ Critical: {len(critical)}")
            if warning:
                print(f"  ⚠️  Warning: {len(warning)}")
        
        # Fixes applied
        if diagnostic_results['fixes_applied']:
            print(f"\nFixes Applied: {len(diagnostic_results['fixes_applied'])}")
            for fix in diagnostic_results['fixes_applied']:
                print(f"  ✅ {fix}")
        
        # Recommendations
        print("\nRECOMMENDATIONS:")
        if health == 'critical':
            print("  🚨 Immediate attention required!")
            print("  - Review critical issues above")
            print("  - Run with auto-fix enabled: python self-diagnostic.py --fix")
            print("  - Consider manual intervention for unresolved issues")
        elif health == 'warning':
            print("  ⚠️  System needs maintenance")
            print("  - Address warning issues when possible")
            print("  - Monitor system performance")
            print("  - Schedule regular diagnostic checks")
        else:
            print("  ✅ System is healthy!")
            print("  - Continue regular monitoring")
            print("  - Keep configurations up to date")
        
        print("\n" + "=" * 60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Ecosystem Self-Diagnostic System")
    parser.add_argument("--fix", action="store_true", help="Enable auto-fix for issues")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    diagnostic = SelfDiagnosticSystem()
    results = diagnostic.run_full_diagnostic(auto_fix=args.fix)
    
    # Exit with appropriate code
    if results['overall_health'] == 'critical':
        sys.exit(2)
    elif results['overall_health'] == 'warning':
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()