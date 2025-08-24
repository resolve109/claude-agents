#!/usr/bin/env python3
"""
Dynamic Agent Spawner - Intelligent Agent Creation System
Detects when new agents are needed and creates them automatically
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import hashlib

class DynamicAgentSpawner:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.agents_path = self.base_path / "agents"
        self.registry_path = self.base_path / "data" / "agent_registry.json"
        self.spawn_log = self.base_path / "data" / "spawn_log.json"
        
        # Domain patterns for auto-detection
        self.domain_patterns = {
            'database': {
                'keywords': ['postgres', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb'],
                'capabilities': ['query optimization', 'schema management', 'backup/recovery', 'replication', 'performance tuning']
            },
            'messaging': {
                'keywords': ['kafka', 'rabbitmq', 'sqs', 'sns', 'pubsub', 'nats', 'activemq'],
                'capabilities': ['message routing', 'queue management', 'topic configuration', 'consumer groups', 'dead letter handling']
            },
            'monitoring': {
                'keywords': ['prometheus', 'grafana', 'datadog', 'newrelic', 'elk', 'splunk', 'cloudwatch'],
                'capabilities': ['metric collection', 'alerting', 'dashboard creation', 'log aggregation', 'performance analysis']
            },
            'networking': {
                'keywords': ['nginx', 'haproxy', 'traefik', 'istio', 'envoy', 'cloudflare', 'cdn'],
                'capabilities': ['load balancing', 'traffic routing', 'ssl management', 'rate limiting', 'caching']
            },
            'storage': {
                'keywords': ['s3', 'gcs', 'azure blob', 'minio', 'ceph', 'gluster', 'nfs'],
                'capabilities': ['object storage', 'file management', 'backup strategies', 'replication', 'lifecycle policies']
            },
            'serverless': {
                'keywords': ['lambda', 'functions', 'fargate', 'cloud run', 'azure functions', 'vercel', 'netlify'],
                'capabilities': ['function deployment', 'event triggers', 'api gateway', 'cold start optimization', 'cost management']
            },
            'ml_ops': {
                'keywords': ['mlflow', 'kubeflow', 'sagemaker', 'tensorflow', 'pytorch', 'model', 'training'],
                'capabilities': ['model deployment', 'experiment tracking', 'pipeline orchestration', 'model versioning', 'inference optimization']
            },
            'testing': {
                'keywords': ['jest', 'pytest', 'selenium', 'cypress', 'junit', 'mocha', 'playwright'],
                'capabilities': ['test automation', 'coverage analysis', 'performance testing', 'integration testing', 'mocking']
            }
        }
        
        self.load_registry()
    
    def load_registry(self):
        """Load the agent registry"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                self.registry = json.load(f)
        else:
            self.registry = {
                'agents': {},
                'capabilities_index': {},
                'registry_version': '1.0.0'
            }
    
    def save_registry(self):
        """Save the updated registry"""
        self.registry['last_updated'] = datetime.now().isoformat()
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def detect_required_agent(self, user_request):
        """Analyze user request to detect if a new agent is needed"""
        request_lower = user_request.lower()
        
        # Check each domain for keyword matches
        for domain, config in self.domain_patterns.items():
            for keyword in config['keywords']:
                if keyword in request_lower:
                    # Check if we already have an agent for this
                    agent_name = keyword.replace(' ', '-')
                    if agent_name not in self.registry.get('agents', {}):
                        return {
                            'needed': True,
                            'domain': domain,
                            'agent_name': agent_name,
                            'keyword': keyword,
                            'capabilities': config['capabilities']
                        }
        
        # Check for explicit agent requests
        agent_request_pattern = r'(create|need|want|require)\s+(?:a\s+|an\s+)?(\w+)\s+agent'
        match = re.search(agent_request_pattern, request_lower)
        if match:
            agent_type = match.group(2)
            if agent_type not in self.registry.get('agents', {}):
                return {
                    'needed': True,
                    'domain': 'custom',
                    'agent_name': agent_type,
                    'keyword': agent_type,
                    'capabilities': self.infer_capabilities(agent_type)
                }
        
        return {'needed': False}
    
    def infer_capabilities(self, agent_type):
        """Infer capabilities based on agent type"""
        base_capabilities = [
            f'{agent_type} configuration',
            f'{agent_type} optimization',
            f'{agent_type} monitoring',
            f'{agent_type} troubleshooting',
            'automation'
        ]
        return base_capabilities
    
    def spawn_agent(self, agent_spec):
        """Create a new agent based on specifications"""
        agent_name = agent_spec['agent_name']
        domain = agent_spec['domain']
        capabilities = agent_spec['capabilities']
        
        print(f"🚀 Spawning new agent: {agent_name}")
        
        # Generate agent configuration
        agent_config = self.generate_agent_config(agent_name, domain, capabilities)
        
        # Create agent file
        agent_file = self.agents_path / f"{agent_name}.md"
        
        # Generate agent content
        agent_content = self.generate_agent_content(agent_config)
        
        # Write agent file
        with open(agent_file, 'w') as f:
            f.write(agent_content)
        
        # Update registry
        self.register_agent(agent_config)
        
        # Log spawn event
        self.log_spawn(agent_config)
        
        print(f"✅ Agent '{agent_name}' successfully spawned!")
        print(f"📍 Location: {agent_file}")
        
        return agent_config
    
    def generate_agent_config(self, name, domain, capabilities):
        """Generate agent configuration"""
        return {
            'name': name,
            'domain': domain,
            'description': f"Dynamically spawned agent for {name} operations",
            'capabilities': capabilities,
            'model': 'inherit',
            'color': self.select_color(),
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'spawned_by': 'Dynamic Agent Spawner',
            'auto_optimize': True,
            'self_healing': True
        }
    
    def select_color(self):
        """Select an appropriate color for the agent"""
        colors = ['blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow']
        used_colors = set()
        
        for agent in self.registry.get('agents', {}).values():
            if 'color' in agent:
                used_colors.add(agent['color'])
        
        available = [c for c in colors if c not in used_colors]
        return available[0] if available else 'blue'
    
    def generate_agent_content(self, config):
        """Generate complete agent markdown content"""
        return f"""---
name: {config['name']}
description: {config['description']}
model: {config['model']}
color: {config['color']}
auto_optimize: {str(config['auto_optimize']).lower()}
self_healing: {str(config['self_healing']).lower()}
version: {config['version']}
spawned_at: {config['created_at']}
spawned_by: {config['spawned_by']}
---

# {config['name'].upper()} Agent

## Identity
**Domain**: {config['domain']}
**Type**: Dynamically Spawned Specialist
**Status**: Active and Learning

## Core Capabilities
{self.format_capabilities(config['capabilities'])}

## Specialized Knowledge Base
```yaml
domain_expertise:
  primary: {config['domain']}
  technology: {config['name']}
  
knowledge_sources:
  - official_documentation
  - best_practices
  - community_patterns
  - learned_experiences
  
continuous_learning:
  enabled: true
  sources:
    - execution_feedback
    - peer_agents
    - user_corrections
    - pattern_recognition
```

## Auto-Optimization Configuration
```yaml
optimization:
  self_learning: enabled
  performance_tracking: active
  
  optimization_triggers:
    - performance_degradation
    - repeated_errors
    - inefficiency_detected
    - new_patterns_found
    
  optimization_actions:
    - update_knowledge_base
    - refine_execution_patterns
    - adjust_parameters
    - request_orchestrator_guidance
```

## Integration Matrix
```yaml
integrations:
  upstream:
    - master  # Supreme orchestrator
    - orchestrator  # Workflow coordination
    
  peer_collaboration:
    # Dynamically discovered based on task requirements
    
  downstream:
    # Service-specific integrations
```

## Execution Framework
```python
class {config['name'].replace('-', '').title()}Agent:
    def __init__(self):
        self.domain = "{config['domain']}"
        self.capabilities = {config['capabilities']}
        self.learning_enabled = True
        self.optimization_active = True
        
    def execute_task(self, task):
        \"\"\"Execute task with learning and optimization\"\"\"
        # Analyze task requirements
        requirements = self.analyze_task(task)
        
        # Check knowledge base
        if self.has_knowledge(requirements):
            solution = self.apply_knowledge(requirements)
        else:
            solution = self.discover_solution(requirements)
            self.learn_from_discovery(solution)
        
        # Execute with monitoring
        result = self.execute_solution(solution)
        
        # Learn from execution
        self.update_knowledge(result)
        
        # Optimize for future
        self.optimize_patterns()
        
        return result
    
    def self_improve(self):
        \"\"\"Continuous self-improvement process\"\"\"
        metrics = self.analyze_performance()
        
        if metrics['efficiency'] < 0.8:
            self.optimize_execution_paths()
        
        if metrics['error_rate'] > 0.05:
            self.enhance_error_handling()
        
        if metrics['response_time'] > 2.0:
            self.improve_response_speed()
        
        return self.measure_improvement()
```

## Performance Metrics
```yaml
performance_targets:
  response_time: <1s
  success_rate: >95%
  learning_rate: continuous
  optimization_frequency: daily
  
current_metrics:
  # Automatically tracked and updated
  response_time: tracking...
  success_rate: tracking...
  total_executions: 0
  patterns_learned: 0
```

## Self-Diagnostic Protocol
```yaml
health_monitoring:
  frequency: continuous
  
  checks:
    - configuration_validity
    - capability_verification
    - performance_metrics
    - error_patterns
    - resource_usage
    
  auto_repair:
    enabled: true
    actions:
      - reset_on_failure
      - clear_error_state
      - optimize_resources
      - request_help_if_needed
```

## Evolution Log
```yaml
evolution_history:
  - version: 1.0.0
    date: {config['created_at']}
    event: "Initial spawn by Dynamic Agent Spawner"
    trigger: "User request for {config['name']} capabilities"
```

## Emergency Protocols
```yaml
failure_handling:
  escalation_path:
    1_self_repair: attempt_auto_fix
    2_peer_help: request_peer_agent_assistance
    3_orchestrator: escalate_to_orchestrator
    4_human: request_human_intervention
    
  fallback_strategies:
    - use_cached_solutions
    - graceful_degradation
    - safe_mode_operation
    - maintenance_mode
```

## Notes
- This agent was dynamically spawned based on detected need
- It includes self-learning and optimization capabilities
- Performance and behavior will improve over time
- The agent will evolve based on usage patterns and feedback
"""
    
    def format_capabilities(self, capabilities):
        """Format capabilities list for markdown"""
        formatted = ""
        for cap in capabilities:
            formatted += f"- **{cap.title()}**: Enabled and continuously improving\n"
        return formatted
    
    def register_agent(self, config):
        """Register the new agent in the registry"""
        self.registry['agents'][config['name']] = {
            'description': config['description'],
            'capabilities': config['capabilities'],
            'status': 'active',
            'version': config['version'],
            'created_at': config['created_at'],
            'spawned_by': config['spawned_by'],
            'domain': config['domain'],
            'color': config['color'],
            'performance': {
                'success_rate': 0,
                'avg_response_time': 0,
                'total_executions': 0
            }
        }
        
        # Update capabilities index
        for capability in config['capabilities']:
            cap_key = capability.lower().replace(' ', '_')
            if cap_key not in self.registry.get('capabilities_index', {}):
                self.registry['capabilities_index'][cap_key] = []
            self.registry['capabilities_index'][cap_key].append(config['name'])
        
        self.save_registry()
    
    def log_spawn(self, config):
        """Log the spawn event"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent_name': config['name'],
            'domain': config['domain'],
            'trigger': 'user_request',
            'capabilities': config['capabilities']
        }
        
        # Load existing log or create new
        if self.spawn_log.exists():
            with open(self.spawn_log, 'r') as f:
                log = json.load(f)
        else:
            log = {'spawns': []}
        
        log['spawns'].append(log_entry)
        
        # Save log
        self.spawn_log.parent.mkdir(exist_ok=True)
        with open(self.spawn_log, 'w') as f:
            json.dump(log, f, indent=2)
    
    def check_and_spawn(self, user_request):
        """Main entry point - check if agent is needed and spawn if required"""
        detection = self.detect_required_agent(user_request)
        
        if detection['needed']:
            print(f"🔍 Detected need for '{detection['agent_name']}' agent")
            agent = self.spawn_agent(detection)
            return {
                'spawned': True,
                'agent': agent,
                'message': f"Successfully spawned {detection['agent_name']} agent"
            }
        else:
            return {
                'spawned': False,
                'message': "No new agent required - existing agents can handle this request"
            }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Dynamic Agent Spawner")
    parser.add_argument("request", nargs='?', help="User request to analyze")
    parser.add_argument("-c", "--create", help="Explicitly create an agent")
    parser.add_argument("-l", "--list", action="store_true", help="List all spawned agents")
    
    args = parser.parse_args()
    
    spawner = DynamicAgentSpawner()
    
    if args.list:
        print("📋 Spawned Agents:")
        for name, info in spawner.registry.get('agents', {}).items():
            if info.get('spawned_by') == 'Dynamic Agent Spawner':
                print(f"  - {name}: {info['description']}")
    elif args.create:
        result = spawner.spawn_agent({
            'agent_name': args.create,
            'domain': 'custom',
            'capabilities': spawner.infer_capabilities(args.create)
        })
        print(f"✅ Agent '{args.create}' created successfully")
    elif args.request:
        result = spawner.check_and_spawn(args.request)
        print(result['message'])
    else:
        print("Usage: agent-spawner.py <user_request>")
        print("       agent-spawner.py --create <agent_name>")
        print("       agent-spawner.py --list")

if __name__ == "__main__":
    main()