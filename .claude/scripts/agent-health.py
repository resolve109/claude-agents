#!/usr/bin/env python3
"""
Agent Health Monitoring System for Claude Ecosystem
Monitors, diagnoses, and repairs agent health issues
"""

import os
import sys
import json
import yaml
import re
from pathlib import Path
from datetime import datetime, timedelta
import time
import hashlib

class AgentHealthMonitor:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.agents_path = self.base_path / "agents"
        self.data_path = self.base_path / "data"
        self.health_log = self.data_path / "health_log.json"
        self.alerts_file = self.data_path / "health_alerts.json"
        
        # Health status definitions
        self.health_states = {
            'healthy': '✅',
            'warning': '⚠️',
            'critical': '❌',
            'unknown': '❓'
        }
        
        # Health check criteria
        self.health_criteria = {
            'config_valid': {'weight': 0.3, 'critical': True},
            'dependencies_met': {'weight': 0.2, 'critical': True},
            'performance_ok': {'weight': 0.2, 'critical': False},
            'no_errors': {'weight': 0.15, 'critical': False},
            'recently_updated': {'weight': 0.1, 'critical': False},
            'version_current': {'weight': 0.05, 'critical': False}
        }
    
    def check_agent_health(self, agent_path):
        """Comprehensive health check for an agent"""
        agent_name = agent_path.stem
        health_status = {
            'agent': agent_name,
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'overall_health': 'unknown',
            'health_score': 0,
            'issues': [],
            'recommendations': []
        }
        
        # Read agent content
        try:
            with open(agent_path, 'r') as f:
                content = f.read()
        except Exception as e:
            health_status['overall_health'] = 'critical'
            health_status['issues'].append(f"Cannot read agent file: {e}")
            return health_status
        
        # Run health checks
        health_status['checks']['config_valid'] = self.check_configuration(content, health_status)
        health_status['checks']['dependencies_met'] = self.check_dependencies(agent_name, health_status)
        health_status['checks']['performance_ok'] = self.check_performance(agent_name, health_status)
        health_status['checks']['no_errors'] = self.check_error_rate(agent_name, health_status)
        health_status['checks']['recently_updated'] = self.check_last_update(agent_path, health_status)
        health_status['checks']['version_current'] = self.check_version(content, health_status)
        
        # Calculate overall health score
        health_score = 0
        critical_failure = False
        
        for check_name, check_result in health_status['checks'].items():
            if check_result:
                health_score += self.health_criteria[check_name]['weight']
            elif self.health_criteria[check_name]['critical']:
                critical_failure = True
        
        health_status['health_score'] = health_score * 100
        
        # Determine overall health status
        if critical_failure:
            health_status['overall_health'] = 'critical'
        elif health_score >= 0.9:
            health_status['overall_health'] = 'healthy'
        elif health_score >= 0.7:
            health_status['overall_health'] = 'warning'
        else:
            health_status['overall_health'] = 'critical'
        
        return health_status
    
    def check_configuration(self, content, health_status):
        """Check if agent configuration is valid"""
        try:
            # Check for frontmatter
            if not content.startswith('---'):
                health_status['issues'].append("Missing YAML frontmatter")
                health_status['recommendations'].append("Add proper YAML frontmatter to agent file")
                return False
            
            # Extract and validate frontmatter
            frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)
                config = yaml.safe_load(frontmatter)
                
                # Check required fields
                required_fields = ['name', 'description']
                for field in required_fields:
                    if field not in config:
                        health_status['issues'].append(f"Missing required field: {field}")
                        health_status['recommendations'].append(f"Add '{field}' to agent configuration")
                        return False
                
                return True
            else:
                health_status['issues'].append("Invalid frontmatter format")
                health_status['recommendations'].append("Fix YAML frontmatter formatting")
                return False
                
        except Exception as e:
            health_status['issues'].append(f"Configuration parsing error: {e}")
            health_status['recommendations'].append("Fix YAML syntax errors in configuration")
            return False
    
    def check_dependencies(self, agent_name, health_status):
        """Check if agent dependencies are met"""
        # Check for MCP server dependencies if applicable
        mcp_config_path = self.base_path / "mcp" / "config.json"
        
        if mcp_config_path.exists():
            try:
                with open(mcp_config_path, 'r') as f:
                    mcp_config = json.load(f)
                    
                # Check if agent has MCP dependencies
                if agent_name in str(mcp_config):
                    # Basic check - can be enhanced
                    return True
            except:
                pass
        
        # Check for environment variables
        env_file = self.base_path / ".env"
        if not env_file.exists():
            health_status['issues'].append("Environment file missing")
            health_status['recommendations'].append("Create .env file with required variables")
            return False
        
        return True
    
    def check_performance(self, agent_name, health_status):
        """Check agent performance metrics"""
        metrics_file = self.data_path / "agent_metrics.json"
        
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    metrics = json.load(f)
                    agent_metrics = metrics.get(agent_name, {})
                    
                    # Check performance thresholds
                    if agent_metrics.get('avg_response_time', 0) > 5.0:
                        health_status['issues'].append("High response time detected")
                        health_status['recommendations'].append("Optimize agent for better performance")
                        return False
                    
                    if agent_metrics.get('success_rate', 1.0) < 0.9:
                        health_status['issues'].append("Low success rate")
                        health_status['recommendations'].append("Investigate and fix failure causes")
                        return False
                    
                    return True
            except:
                pass
        
        # No metrics available - assume healthy
        return True
    
    def check_error_rate(self, agent_name, health_status):
        """Check agent error rate"""
        metrics_file = self.data_path / "agent_metrics.json"
        
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    metrics = json.load(f)
                    agent_metrics = metrics.get(agent_name, {})
                    
                    error_rate = agent_metrics.get('error_rate', 0)
                    if error_rate > 0.1:  # More than 10% errors
                        health_status['issues'].append(f"High error rate: {error_rate:.1%}")
                        health_status['recommendations'].append("Add better error handling")
                        return False
                    
                    return True
            except:
                pass
        
        return True
    
    def check_last_update(self, agent_path, health_status):
        """Check when agent was last updated"""
        try:
            mtime = os.path.getmtime(agent_path)
            last_update = datetime.fromtimestamp(mtime)
            days_old = (datetime.now() - last_update).days
            
            if days_old > 30:
                health_status['issues'].append(f"Agent not updated in {days_old} days")
                health_status['recommendations'].append("Review and update agent configuration")
                return False
            
            return True
        except:
            return True
    
    def check_version(self, content, health_status):
        """Check if agent version is current"""
        # Look for version in frontmatter
        version_match = re.search(r'version:\s*([^\n]+)', content)
        
        if not version_match:
            health_status['issues'].append("No version information")
            health_status['recommendations'].append("Add version tracking to agent")
            return False
        
        return True
    
    def auto_repair(self, agent_path, health_status):
        """Attempt to auto-repair agent issues"""
        repairs_made = []
        agent_name = agent_path.stem
        
        try:
            with open(agent_path, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # Auto-repair missing frontmatter
            if "Missing YAML frontmatter" in str(health_status['issues']):
                frontmatter = f"""---
name: {agent_name}
description: Agent for {agent_name} operations
model: inherit
color: blue
auto_optimize: true
self_healing: enabled
---

"""
                content = frontmatter + content
                repairs_made.append("Added missing frontmatter")
            
            # Auto-repair missing version
            if "No version information" in str(health_status['issues']):
                if content.startswith('---'):
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.strip() == '---' and i > 0:
                            lines.insert(i, f"version: {datetime.now().strftime('%Y.%m.%d')}")
                            content = '\n'.join(lines)
                            repairs_made.append("Added version information")
                            break
            
            # Auto-repair performance issues
            if "High response time" in str(health_status['issues']):
                if 'caching:' not in content:
                    cache_config = """
## Performance Optimization
```yaml
caching:
  enabled: true
  strategy: aggressive
```
"""
                    content += "\n" + cache_config
                    repairs_made.append("Added caching configuration")
            
            # Write repairs if any were made
            if content != original_content:
                # Backup original
                backup_path = self.data_path / "backups" / f"{agent_name}_health_repair_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                backup_path.write_text(original_content)
                
                # Write repaired content
                agent_path.write_text(content)
                
                return True, repairs_made
                
        except Exception as e:
            return False, [f"Repair failed: {e}"]
        
        return False, []
    
    def monitor_all_agents(self, auto_repair=False):
        """Monitor health of all agents"""
        print("🏥 Starting Agent Health Check...")
        print("=" * 50)
        
        agents = list(self.agents_path.glob("*.md"))
        agents = [a for a in agents if a.name not in ["AGENT_TEMPLATE.md", "README.md"]]
        
        health_results = []
        alerts = []
        
        for agent_path in agents:
            agent_name = agent_path.stem
            print(f"\n🔍 Checking: {agent_name}")
            
            # Run health check
            health_status = self.check_agent_health(agent_path)
            health_results.append(health_status)
            
            # Display status
            status_icon = self.health_states[health_status['overall_health']]
            print(f"  Status: {status_icon} {health_status['overall_health'].upper()}")
            print(f"  Health Score: {health_status['health_score']:.1f}/100")
            
            # Display checks
            for check, result in health_status['checks'].items():
                check_icon = "✅" if result else "❌"
                print(f"    {check_icon} {check.replace('_', ' ').title()}")
            
            # Handle critical issues
            if health_status['overall_health'] == 'critical':
                alerts.append({
                    'agent': agent_name,
                    'severity': 'critical',
                    'issues': health_status['issues'],
                    'timestamp': datetime.now().isoformat()
                })
                
                if auto_repair:
                    print(f"  🔧 Attempting auto-repair...")
                    repaired, repairs = self.auto_repair(agent_path, health_status)
                    if repaired:
                        print(f"  ✅ Auto-repair successful:")
                        for repair in repairs:
                            print(f"     - {repair}")
                    else:
                        print(f"  ❌ Auto-repair failed")
            
            # Display issues
            if health_status['issues']:
                print(f"  Issues:")
                for issue in health_status['issues']:
                    print(f"    ⚠️  {issue}")
            
            # Display recommendations
            if health_status['recommendations']:
                print(f"  Recommendations:")
                for rec in health_status['recommendations']:
                    print(f"    💡 {rec}")
        
        # Save health log
        self.save_health_log(health_results)
        
        # Save alerts if any
        if alerts:
            self.save_alerts(alerts)
            print(f"\n🚨 {len(alerts)} CRITICAL ALERTS logged")
        
        # Generate summary
        self.display_summary(health_results)
        
        return health_results
    
    def save_health_log(self, health_results):
        """Save health check results to log"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'results': health_results
        }
        
        # Load existing log or create new
        if self.health_log.exists():
            with open(self.health_log, 'r') as f:
                log = json.load(f)
        else:
            log = {'checks': []}
        
        log['checks'].append(log_entry)
        
        # Keep only last 50 checks
        if len(log['checks']) > 50:
            log['checks'] = log['checks'][-50:]
        
        # Save log
        self.health_log.parent.mkdir(exist_ok=True)
        with open(self.health_log, 'w') as f:
            json.dump(log, f, indent=2)
    
    def save_alerts(self, alerts):
        """Save critical alerts"""
        # Load existing alerts or create new
        if self.alerts_file.exists():
            with open(self.alerts_file, 'r') as f:
                all_alerts = json.load(f)
        else:
            all_alerts = {'alerts': []}
        
        all_alerts['alerts'].extend(alerts)
        
        # Keep only last 100 alerts
        if len(all_alerts['alerts']) > 100:
            all_alerts['alerts'] = all_alerts['alerts'][-100:]
        
        # Save alerts
        self.alerts_file.parent.mkdir(exist_ok=True)
        with open(self.alerts_file, 'w') as f:
            json.dump(all_alerts, f, indent=2)
    
    def display_summary(self, health_results):
        """Display health check summary"""
        print("\n" + "=" * 50)
        print("📊 HEALTH CHECK SUMMARY")
        print("=" * 50)
        
        # Count by status
        status_counts = {
            'healthy': 0,
            'warning': 0,
            'critical': 0,
            'unknown': 0
        }
        
        for result in health_results:
            status_counts[result['overall_health']] += 1
        
        # Calculate average health score
        avg_score = sum(r['health_score'] for r in health_results) / len(health_results) if health_results else 0
        
        print(f"\nTotal Agents: {len(health_results)}")
        print(f"Average Health Score: {avg_score:.1f}/100")
        print("\nStatus Breakdown:")
        for status, count in status_counts.items():
            if count > 0:
                icon = self.health_states[status]
                percentage = (count / len(health_results)) * 100
                print(f"  {icon} {status.title()}: {count} ({percentage:.1f}%)")
        
        # Overall system health
        if status_counts['critical'] > 0:
            print(f"\n🚨 SYSTEM HEALTH: CRITICAL - {status_counts['critical']} agents need attention")
        elif status_counts['warning'] > 0:
            print(f"\n⚠️  SYSTEM HEALTH: WARNING - {status_counts['warning']} agents have issues")
        else:
            print("\n✅ SYSTEM HEALTH: EXCELLENT - All agents healthy")
        
        print("\n" + "=" * 50)
    
    def continuous_monitoring(self, interval=60, auto_repair=True):
        """Run continuous health monitoring"""
        print(f"🔄 Starting continuous monitoring (interval: {interval}s)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.monitor_all_agents(auto_repair=auto_repair)
                print(f"\n⏰ Next check in {interval} seconds...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor and repair agent health")
    parser.add_argument("-c", "--continuous", action="store_true", 
                       help="Run continuous monitoring")
    parser.add_argument("-i", "--interval", type=int, default=60,
                       help="Monitoring interval in seconds (default: 60)")
    parser.add_argument("-r", "--repair", action="store_true",
                       help="Enable auto-repair of issues")
    parser.add_argument("-a", "--agent", help="Check specific agent only")
    
    args = parser.parse_args()
    
    monitor = AgentHealthMonitor()
    
    if args.continuous:
        monitor.continuous_monitoring(interval=args.interval, auto_repair=args.repair)
    elif args.agent:
        agent_path = monitor.agents_path / f"{args.agent}.md"
        if agent_path.exists():
            health_status = monitor.check_agent_health(agent_path)
            print(json.dumps(health_status, indent=2))
        else:
            print(f"❌ Agent '{args.agent}' not found")
    else:
        monitor.monitor_all_agents(auto_repair=args.repair)

if __name__ == "__main__":
    main()