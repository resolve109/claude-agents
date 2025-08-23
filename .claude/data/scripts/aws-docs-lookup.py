#!/usr/bin/env python3
"""
AWS Documentation Lookup Tool - Python version
Provides easy access to AWS service documentation references
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Base paths
BASE_DIR = Path("/mnt/e/github/agents/claude-agents/.claude/data/shared/references/aws-docs")
MASTER_INDEX = BASE_DIR / "master-index.json"

# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

def load_index() -> Dict:
    """Load the master index file"""
    try:
        with open(MASTER_INDEX, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Colors.RED}Error: Master index not found at {MASTER_INDEX}{Colors.NC}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}Error: Invalid JSON in master index: {e}{Colors.NC}")
        sys.exit(1)

def get_service(service_name: str) -> None:
    """Get information about a specific service"""
    index = load_index()
    
    if service_name not in index["services"]:
        print(f"{Colors.RED}Service '{service_name}' not found{Colors.NC}")
        print(f"Use 'list-services' to see available services")
        return
    
    service = index["services"][service_name]
    print(f"{Colors.GREEN}Service: {Colors.NC}{service['name']}")
    print(f"{Colors.BLUE}Description: {Colors.NC}{service['description']}")
    print(f"{Colors.YELLOW}Category: {Colors.NC}{service['category']}")
    print(f"{Colors.CYAN}PDF URL: {Colors.NC}{service['pdf_url']}")
    
    # Check if category-specific index exists with more details
    category_index = BASE_DIR / "indexes" / f"{service['category']}.json"
    if category_index.exists():
        with open(category_index, 'r') as f:
            cat_data = json.load(f)
            if service_name in cat_data.get("services", {}):
                service_details = cat_data["services"][service_name]
                if "key_topics" in service_details:
                    print(f"\n{Colors.GREEN}Key Topics:{Colors.NC}")
                    for topic in service_details["key_topics"]:
                        print(f"  • {topic}")

def get_category(category_name: str) -> None:
    """List all services in a category"""
    index = load_index()
    
    if category_name not in index["categories"]:
        print(f"{Colors.RED}Category '{category_name}' not found{Colors.NC}")
        print(f"Use 'list-categories' to see available categories")
        return
    
    category = index["categories"][category_name]
    print(f"{Colors.GREEN}Category: {Colors.NC}{category['name']}")
    print(f"{Colors.BLUE}Services in this category:{Colors.NC}\n")
    
    for service_key in category["services"]:
        if service_key in index["services"]:
            service = index["services"][service_key]
            print(f"  • {service['name']} ({service_key})")
            print(f"    {service['description']}\n")

def search_services(search_term: str) -> None:
    """Search for services matching a term"""
    index = load_index()
    term_lower = search_term.lower()
    
    print(f"{Colors.GREEN}Searching for: {Colors.NC}{search_term}\n")
    
    matches = []
    for key, service in index["services"].items():
        if (term_lower in key.lower() or 
            term_lower in service["name"].lower() or 
            term_lower in service["description"].lower()):
            matches.append((key, service))
    
    if not matches:
        print(f"{Colors.YELLOW}No services found matching '{search_term}'{Colors.NC}")
        return
    
    print(f"Found {len(matches)} matching service(s):\n")
    for key, service in matches:
        print(f"  • {service['name']} ({key})")
        print(f"    {service['description']}")
        print(f"    Category: {service['category']}\n")

def list_categories() -> None:
    """List all available categories"""
    index = load_index()
    
    print(f"{Colors.GREEN}Available Categories:{Colors.NC}\n")
    
    for key, category in index["categories"].items():
        print(f"  • {category['name']} ({key})")
        services = ", ".join(category["services"][:5])
        if len(category["services"]) > 5:
            services += f", ... (+{len(category['services'])-5} more)"
        print(f"    Services: {services}\n")

def list_services() -> None:
    """List all available services"""
    index = load_index()
    
    print(f"{Colors.GREEN}Available AWS Services:{Colors.NC}\n")
    
    # Group by category for better organization
    by_category = {}
    for key, service in index["services"].items():
        category = service["category"]
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((key, service["name"]))
    
    for category in sorted(by_category.keys()):
        cat_name = index["categories"][category]["name"] if category in index["categories"] else category
        print(f"{Colors.YELLOW}{cat_name}:{Colors.NC}")
        for key, name in sorted(by_category[category], key=lambda x: x[1]):
            print(f"  • {name} ({key})")
        print()

def download_service(service_name: str) -> None:
    """Download PDF for a service (prints command to use)"""
    index = load_index()
    
    if service_name not in index["services"]:
        print(f"{Colors.RED}Service '{service_name}' not found{Colors.NC}")
        return
    
    service = index["services"][service_name]
    pdf_url = service["pdf_url"]
    pdf_path = BASE_DIR / "pdfs" / f"{service_name}.pdf"
    
    print(f"{Colors.GREEN}To download PDF for {service['name']}:{Colors.NC}")
    print(f"\nUsing wget:")
    print(f"  wget -O '{pdf_path}' '{pdf_url}'")
    print(f"\nUsing curl:")
    print(f"  curl -L -o '{pdf_path}' '{pdf_url}'")
    print(f"\nOr use the converter script:")
    print(f"  python3 {BASE_DIR.parent.parent.parent / 'scripts/aws-docs-converter.py'} service {service_name}")

def convert_service(service_name: str) -> None:
    """Convert PDF to text for a service (prints command to use)"""
    index = load_index()
    
    if service_name not in index["services"]:
        print(f"{Colors.RED}Service '{service_name}' not found{Colors.NC}")
        return
    
    pdf_path = BASE_DIR / "pdfs" / f"{service_name}.pdf"
    text_path = BASE_DIR / "text" / f"{service_name}.txt"
    
    print(f"{Colors.GREEN}To convert PDF to text for {index['services'][service_name]['name']}:{Colors.NC}")
    print(f"\nUsing pdftotext:")
    print(f"  pdftotext '{pdf_path}' '{text_path}'")
    print(f"\nUsing Python converter script:")
    print(f"  python3 {BASE_DIR.parent.parent.parent / 'scripts/aws-docs-converter.py'} service {service_name} --convert-only")
    
    if not pdf_path.exists():
        print(f"\n{Colors.YELLOW}Note: PDF not yet downloaded. Download it first using:{Colors.NC}")
        print(f"  python3 {sys.argv[0]} download {service_name}")

def show_stats() -> None:
    """Show statistics about the documentation collection"""
    index = load_index()
    
    total_services = len(index["services"])
    total_categories = len(index["categories"])
    
    # Count existing files
    pdf_count = len(list((BASE_DIR / "pdfs").glob("*.pdf"))) if (BASE_DIR / "pdfs").exists() else 0
    text_count = len(list((BASE_DIR / "text").glob("*.txt"))) if (BASE_DIR / "text").exists() else 0
    
    print(f"{Colors.GREEN}AWS Documentation Statistics:{Colors.NC}\n")
    print(f"Total services indexed: {total_services}")
    print(f"Total categories: {total_categories}")
    print(f"PDFs downloaded: {pdf_count}/{total_services} ({pdf_count*100//total_services}%)")
    print(f"Texts converted: {text_count}/{total_services} ({text_count*100//total_services}%)")
    
    # Show category breakdown
    print(f"\n{Colors.YELLOW}Services per category:{Colors.NC}")
    for key, category in index["categories"].items():
        print(f"  • {category['name']}: {len(category['services'])} services")

def main():
    parser = argparse.ArgumentParser(
        description="AWS Documentation Lookup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s service ec2           - Get info about EC2 service
  %(prog)s category networking    - List networking services
  %(prog)s search lambda         - Search for lambda-related services
  %(prog)s list-categories      - List all categories
  %(prog)s list-services         - List all services
  %(prog)s stats                 - Show documentation statistics
        """
    )
    
    parser.add_argument("command", 
                       choices=["service", "category", "search", "list-categories", 
                               "list-services", "download", "convert", "stats"],
                       help="Command to execute")
    parser.add_argument("query", nargs="?", help="Service name, category, or search term")
    
    args = parser.parse_args()
    
    if args.command == "service":
        if not args.query:
            print(f"{Colors.RED}Error: Service name required{Colors.NC}")
            sys.exit(1)
        get_service(args.query)
    elif args.command == "category":
        if not args.query:
            print(f"{Colors.RED}Error: Category name required{Colors.NC}")
            sys.exit(1)
        get_category(args.query)
    elif args.command == "search":
        if not args.query:
            print(f"{Colors.RED}Error: Search term required{Colors.NC}")
            sys.exit(1)
        search_services(args.query)
    elif args.command == "list-categories":
        list_categories()
    elif args.command == "list-services":
        list_services()
    elif args.command == "download":
        if not args.query:
            print(f"{Colors.RED}Error: Service name required{Colors.NC}")
            sys.exit(1)
        download_service(args.query)
    elif args.command == "convert":
        if not args.query:
            print(f"{Colors.RED}Error: Service name required{Colors.NC}")
            sys.exit(1)
        convert_service(args.query)
    elif args.command == "stats":
        show_stats()

if __name__ == "__main__":
    main()