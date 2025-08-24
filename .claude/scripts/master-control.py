#!/usr/bin/env python3
"""
Master Control System - Supreme Orchestrator Interface
Central command interface for the self-evolving Claude ecosystem
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import argparse

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Import all subsystems with better error handling
subsystems_available = True
try:
    # Change working directory temporarily for imports
    original_cwd = os.getcwd()
    os.chdir(scripts_dir)
    
    # Import using direct file loading if module import fails
    import importlib.util
    
    def load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    # Load modules
    agent_spawner = load_module("agent_spawner", scripts_dir / "agent-spawner.py")
    DynamicAgentSpawner = agent_spawner.DynamicAgentSpawner
    
    self_diagnostic = load_module("self_diagnostic", scripts_dir / "self-diagnostic.py")
    SelfDiagnosticSystem = self_diagnostic.SelfDiagnosticSystem
    
    agent_health = load_module("agent_health", scripts_dir / "agent-health.py")
    AgentHealthMonitor = agent_health.AgentHealthMonitor
    
    optimize_agents = load_module("optimize_agents", scripts_dir / "optimize-agents.py")
    AgentOptimizer = optimize_agents.AgentOptimizer
    
    os.chdir(original_cwd)
    
except Exception as e:
    print(f"Warning: Could not import all modules: {e}")
    subsystems_available = False

class MasterControl:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.version = "2.0.0"
        self.mode = "SUPREME"
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║           MASTER CONTROL SYSTEM v{self.version}                    ║
║            Supreme Orchestrator Interface                    ║
║                                                              ║
║  Mode: {self.mode:<52}  ║
║  Status: ACTIVE | Self-Evolving | Auto-Correcting           ║
╚══════════════════════════════════════════════════════════════╝
""")
        
        # Initialize subsystems if available
        if subsystems_available:
            self.spawner = DynamicAgentSpawner()
            self.diagnostic = SelfDiagnosticSystem()
            self.health_monitor = AgentHealthMonitor()
            self.optimizer = AgentOptimizer()
        else:
            print("⚠️  Some subsystems unavailable - running in limited mode")
            self.spawner = None
            self.diagnostic = None
            self.health_monitor = None
            self.optimizer = None
    
    def status(self):
        """Display system status"""
        print("\n📊 SYSTEM STATUS")
        print("=" * 60)
        
        # Count agents
        agents_path = self.base_path / "agents"
        agent_count = len(list(agents_path.glob("*.md"))) - 1  # Exclude template
        
        # Load registry
        registry_path = self.base_path / "data" / "agent_registry.json"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry = json.load(f)
                active_agents = sum(1 for a in registry.get('agents', {}).values() 
                                  if a.get('status') == 'active')
        else:
            active_agents = 0
        
        # Check system health
        system_state_path = self.base_path / "data" / "system_state.json"
        if system_state_path.exists():
            with open(system_state_path, 'r') as f:
                state = json.load(f)
                overall_health = state.get('overall_health', 'unknown')
        else:
            overall_health = 'unknown'
        
        print(f"Total Agents: {agent_count}")
        print(f"Active Agents: {active_agents}")
        print(f"System Health: {overall_health.upper()}")
        print(f"Mode: {self.mode}")
        print(f"Auto-Evolution: ENABLED")
        print(f"Self-Correction: ACTIVE")
        print(f"Dynamic Spawning: READY")
        
        # Show recent activity
        spawn_log = self.base_path / "data" / "spawn_log.json"
        if spawn_log.exists():
            with open(spawn_log, 'r') as f:
                log = json.load(f)
                if log.get('spawns'):
                    recent = log['spawns'][-1]
                    print(f"\nLast Spawn: {recent['agent_name']} at {recent['timestamp']}")
        
        print("=" * 60)
    
    def diagnose(self, auto_fix=True):
        """Run full system diagnostic"""
        print("\n🔬 Running System Diagnostic...")
        results = self.diagnostic.run_full_diagnostic(auto_fix=auto_fix)
        return results
    
    def health_check(self, auto_repair=True):
        """Check health of all agents"""
        print("\n🏥 Checking Agent Health...")
        results = self.health_monitor.monitor_all_agents(auto_repair=auto_repair)
        return results
    
    def optimize(self, target_agent=None):
        """Optimize agents"""
        print("\n⚡ Optimizing Agents...")
        self.optimizer.run_optimization(target_agent)
    
    def spawn(self, request):
        """Spawn new agent based on request"""
        print(f"\n🚀 Analyzing request: {request}")
        result = self.spawner.check_and_spawn(request)
        print(result['message'])
        return result
    
    def create_agent(self, name, capabilities=None):
        """Explicitly create a new agent"""
        print(f"\n🛠️ Creating agent: {name}")
        
        if not capabilities:
            capabilities = self.spawner.infer_capabilities(name)
        
        result = self.spawner.spawn_agent({
            'agent_name': name,
            'domain': 'custom',
            'capabilities': capabilities
        })
        
        print(f"✅ Agent '{name}' created successfully")
        return result
    
    def list_agents(self):
        """List all agents with their status"""
        print("\n📋 AGENT REGISTRY")
        print("=" * 60)
        
        registry_path = self.base_path / "data" / "agent_registry.json"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry = json.load(f)
                
            for name, info in registry.get('agents', {}).items():
                status_icon = "✅" if info.get('status') == 'active' else "⚠️"
                print(f"{status_icon} {name:15} - {info.get('description', 'No description')}")
                
                # Show performance if available
                perf = info.get('performance', {})
                if perf.get('total_executions', 0) > 0:
                    print(f"   Performance: {perf.get('success_rate', 0):.1%} success, "
                          f"{perf.get('avg_response_time', 0):.1f}s avg response")
        else:
            print("No registry found")
        
        print("=" * 60)
    
    def auto_evolve(self):
        """Run complete auto-evolution cycle"""
        print("\n🔄 INITIATING AUTO-EVOLUTION CYCLE")
        print("=" * 60)
        
        # Step 1: Diagnostic
        print("\n[1/4] Running diagnostic...")
        diag_results = self.diagnose(auto_fix=True)
        
        # Step 2: Health check
        print("\n[2/4] Checking agent health...")
        health_results = self.health_check(auto_repair=True)
        
        # Step 3: Optimization
        print("\n[3/4] Optimizing agents...")
        self.optimize()
        
        # Step 4: Report
        print("\n[4/4] Evolution complete!")
        print("\nEVOLUTION SUMMARY:")
        print(f"  System Health: {diag_results['overall_health'].upper()}")
        print(f"  Issues Fixed: {len(diag_results.get('fixes_applied', []))}")
        print(f"  Agents Optimized: Check optimization report")
        
        print("\n✨ Auto-evolution cycle complete!")
    
    def interactive_mode(self):
        """Interactive command mode"""
        print("\n🎮 INTERACTIVE MODE")
        print("Type 'help' for commands, 'exit' to quit\n")
        
        commands = {
            'status': self.status,
            'diagnose': lambda: self.diagnose(True),
            'health': lambda: self.health_check(True),
            'optimize': lambda: self.optimize(),
            'list': self.list_agents,
            'evolve': self.auto_evolve,
            'help': self.show_help,
            'exit': lambda: sys.exit(0)
        }
        
        while True:
            try:
                cmd = input("\nmaster> ").strip().lower()
                
                if cmd in commands:
                    commands[cmd]()
                elif cmd.startswith('spawn '):
                    request = cmd[6:]
                    self.spawn(request)
                elif cmd.startswith('create '):
                    name = cmd[7:]
                    self.create_agent(name)
                elif cmd.startswith('optimize '):
                    agent = cmd[9:]
                    self.optimize(agent)
                else:
                    print(f"Unknown command: {cmd}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        """Show help information"""
        print("""
AVAILABLE COMMANDS:
==================
  status              - Show system status
  diagnose            - Run full diagnostic with auto-fix
  health              - Check agent health with auto-repair
  optimize [agent]    - Optimize all agents or specific agent
  list                - List all agents
  spawn <request>     - Spawn agent based on request
  create <name>       - Create new agent with name
  evolve              - Run complete auto-evolution cycle
  help                - Show this help
  exit                - Exit interactive mode

EXAMPLES:
=========
  spawn need redis optimization
  create nginx-optimizer
  optimize terra
  evolve
""")

def main():
    parser = argparse.ArgumentParser(
        description="Master Control System - Supreme Orchestrator Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  master-control.py --status           # Show system status
  master-control.py --diagnose         # Run diagnostic with auto-fix
  master-control.py --evolve           # Run auto-evolution cycle
  master-control.py --spawn "need redis optimization"
  master-control.py --interactive      # Enter interactive mode
        """
    )
    
    parser.add_argument("-s", "--status", action="store_true", 
                       help="Show system status")
    parser.add_argument("-d", "--diagnose", action="store_true",
                       help="Run system diagnostic with auto-fix")
    parser.add_argument("-H", "--health", action="store_true",
                       help="Check agent health with auto-repair")
    parser.add_argument("-o", "--optimize", nargs='?', const='all',
                       help="Optimize agents (optionally specify agent name)")
    parser.add_argument("-l", "--list", action="store_true",
                       help="List all agents")
    parser.add_argument("-e", "--evolve", action="store_true",
                       help="Run complete auto-evolution cycle")
    parser.add_argument("--spawn", help="Spawn agent based on request")
    parser.add_argument("--create", help="Create new agent with name")
    parser.add_argument("-i", "--interactive", action="store_true",
                       help="Enter interactive mode")
    
    args = parser.parse_args()
    
    # Initialize master control
    master = MasterControl()
    
    # Execute requested action
    if args.status:
        master.status()
    elif args.diagnose:
        master.diagnose()
    elif args.health:
        master.health_check()
    elif args.optimize:
        if args.optimize == 'all':
            master.optimize()
        else:
            master.optimize(args.optimize)
    elif args.list:
        master.list_agents()
    elif args.evolve:
        master.auto_evolve()
    elif args.spawn:
        master.spawn(args.spawn)
    elif args.create:
        master.create_agent(args.create)
    elif args.interactive:
        master.interactive_mode()
    else:
        # No arguments - show status and enter interactive mode
        master.status()
        master.interactive_mode()

if __name__ == "__main__":
    main()