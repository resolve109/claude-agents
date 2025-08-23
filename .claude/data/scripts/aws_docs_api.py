#!/usr/bin/env python3
"""
AWS Documentation API
Provides programmatic access to AWS service documentation URLs
"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path

class AWSDocsAPI:
    """API for accessing AWS documentation URLs and metadata"""
    
    def __init__(self, data_dir: str = None):
        """Initialize the AWS Docs API
        
        Args:
            data_dir: Path to the AWS docs data directory. 
                     Defaults to .claude/data/aws-docs
        """
        if data_dir is None:
            # Get the base directory relative to this script
            base_dir = Path(__file__).resolve().parent.parent.parent
            data_dir = base_dir / "data" / "aws-docs"
        else:
            data_dir = Path(data_dir)
        
        self.data_dir = data_dir
        self._load_data()
    
    def _load_data(self):
        """Load all JSON data files"""
        # Load services master data
        services_file = self.data_dir / "services-master.json"
        with open(services_file, 'r') as f:
            services_data = json.load(f)
            self.services = services_data.get('services', {})
            self.metadata = services_data.get('metadata', {})
        
        # Load categories index
        categories_file = self.data_dir / "categories-index.json"
        with open(categories_file, 'r') as f:
            categories_data = json.load(f)
            self.categories = categories_data.get('categories', {})
        
        # Load tags index
        tags_file = self.data_dir / "tags-index.json"
        with open(tags_file, 'r') as f:
            tags_data = json.load(f)
            self.tags = tags_data.get('tags', {})
    
    def get_service_url(self, service: str) -> Optional[str]:
        """Get the PDF URL for a specific service
        
        Args:
            service: Service identifier (e.g., 'ec2', 's3', 'lambda')
        
        Returns:
            PDF URL string or None if service not found
        """
        service_data = self.services.get(service)
        if service_data:
            return service_data.get('pdf_url')
        return None
    
    def get_service_info(self, service: str) -> Optional[Dict[str, Any]]:
        """Get complete information about a service
        
        Args:
            service: Service identifier
        
        Returns:
            Dictionary with service information or None if not found
        """
        return self.services.get(service)
    
    def list_all_services(self) -> List[str]:
        """Get a list of all available service identifiers
        
        Returns:
            List of service identifiers
        """
        return list(self.services.keys())
    
    def get_services_by_category(self, category: str) -> List[str]:
        """Get all services in a specific category
        
        Args:
            category: Category name (e.g., 'compute', 'storage')
        
        Returns:
            List of service identifiers in the category
        """
        cat_data = self.categories.get(category, {})
        return cat_data.get('services', [])
    
    def get_services_by_tag(self, tag: str) -> List[str]:
        """Get all services with a specific tag
        
        Args:
            tag: Tag name (e.g., 'serverless', 'security')
        
        Returns:
            List of service identifiers with the tag
        """
        return self.tags.get(tag, [])
    
    def search_services(self, term: str) -> List[Dict[str, Any]]:
        """Search for services by name, tag, or category
        
        Args:
            term: Search term
        
        Returns:
            List of matching services with their information
        """
        term_lower = term.lower()
        results = []
        
        for service_id, service_data in self.services.items():
            # Search in service ID
            if term_lower in service_id.lower():
                results.append({'id': service_id, **service_data})
                continue
            
            # Search in service name
            if term_lower in service_data.get('name', '').lower():
                results.append({'id': service_id, **service_data})
                continue
            
            # Search in category
            if term_lower in service_data.get('category', '').lower():
                results.append({'id': service_id, **service_data})
                continue
            
            # Search in tags
            tags = service_data.get('tags', [])
            for tag in tags:
                if term_lower in tag.lower():
                    results.append({'id': service_id, **service_data})
                    break
        
        return results
    
    def get_all_categories(self) -> Dict[str, Any]:
        """Get all categories with their descriptions
        
        Returns:
            Dictionary of categories
        """
        return self.categories
    
    def get_all_tags(self) -> List[str]:
        """Get all available tags
        
        Returns:
            List of tag names
        """
        return list(self.tags.keys())
    
    def get_services_by_subcategory(self, category: str, subcategory: str) -> List[str]:
        """Get services in a specific subcategory
        
        Args:
            category: Main category name
            subcategory: Subcategory name
        
        Returns:
            List of service identifiers
        """
        cat_data = self.categories.get(category, {})
        subcategories = cat_data.get('subcategories', {})
        return subcategories.get(subcategory, [])
    
    def get_terraform_resources(self, service: str) -> Dict[str, str]:
        """Get common Terraform resource types for a service
        
        Args:
            service: Service identifier
        
        Returns:
            Dictionary mapping resource types to descriptions
        """
        # Common Terraform resource mappings
        terraform_mappings = {
            'ec2': {
                'aws_instance': 'EC2 instance',
                'aws_security_group': 'Security group',
                'aws_key_pair': 'SSH key pair',
                'aws_eip': 'Elastic IP',
                'aws_ami': 'Amazon Machine Image'
            },
            's3': {
                'aws_s3_bucket': 'S3 bucket',
                'aws_s3_bucket_policy': 'Bucket policy',
                'aws_s3_bucket_versioning': 'Bucket versioning',
                'aws_s3_bucket_encryption': 'Bucket encryption',
                'aws_s3_object': 'S3 object'
            },
            'vpc': {
                'aws_vpc': 'Virtual Private Cloud',
                'aws_subnet': 'VPC subnet',
                'aws_internet_gateway': 'Internet gateway',
                'aws_nat_gateway': 'NAT gateway',
                'aws_route_table': 'Route table'
            },
            'rds': {
                'aws_db_instance': 'RDS instance',
                'aws_db_subnet_group': 'DB subnet group',
                'aws_db_parameter_group': 'DB parameter group',
                'aws_db_cluster': 'Aurora cluster'
            },
            'lambda': {
                'aws_lambda_function': 'Lambda function',
                'aws_lambda_layer_version': 'Lambda layer',
                'aws_lambda_permission': 'Lambda permission',
                'aws_lambda_event_source_mapping': 'Event source mapping'
            },
            'iam': {
                'aws_iam_user': 'IAM user',
                'aws_iam_role': 'IAM role',
                'aws_iam_policy': 'IAM policy',
                'aws_iam_group': 'IAM group',
                'aws_iam_instance_profile': 'Instance profile'
            }
        }
        
        return terraform_mappings.get(service, {})
    
    def generate_reference_card(self, services: List[str]) -> str:
        """Generate a quick reference card for specified services
        
        Args:
            services: List of service identifiers
        
        Returns:
            Formatted reference card as string
        """
        card = "AWS Services Quick Reference\n"
        card += "=" * 50 + "\n\n"
        
        for service_id in services:
            service_data = self.services.get(service_id)
            if service_data:
                card += f"Service: {service_data['name']} ({service_id})\n"
                card += f"Category: {service_data['category']}\n"
                card += f"PDF: {service_data['pdf_url']}\n"
                card += f"Tags: {', '.join(service_data['tags'])}\n"
                card += "-" * 30 + "\n\n"
        
        return card


# CLI interface when run directly
if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='AWS Documentation API CLI')
    parser.add_argument('command', choices=['url', 'info', 'list', 'search', 'category', 'tag'],
                       help='Command to execute')
    parser.add_argument('argument', nargs='?', help='Argument for the command')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    args = parser.parse_args()
    
    # Initialize API
    api = AWSDocsAPI()
    
    # Execute command
    if args.command == 'url':
        if not args.argument:
            print("Error: Service name required")
            sys.exit(1)
        url = api.get_service_url(args.argument)
        if url:
            if args.json:
                print(json.dumps({'service': args.argument, 'url': url}))
            else:
                print(url)
        else:
            print(f"Service '{args.argument}' not found")
            sys.exit(1)
    
    elif args.command == 'info':
        if not args.argument:
            print("Error: Service name required")
            sys.exit(1)
        info = api.get_service_info(args.argument)
        if info:
            if args.json:
                print(json.dumps(info, indent=2))
            else:
                print(f"Name: {info['name']}")
                print(f"Category: {info['category']}")
                print(f"Subcategory: {info['subcategory']}")
                print(f"URL: {info['pdf_url']}")
                print(f"Tags: {', '.join(info['tags'])}")
        else:
            print(f"Service '{args.argument}' not found")
            sys.exit(1)
    
    elif args.command == 'list':
        services = api.list_all_services()
        if args.json:
            print(json.dumps(services))
        else:
            for service in sorted(services):
                print(service)
    
    elif args.command == 'search':
        if not args.argument:
            print("Error: Search term required")
            sys.exit(1)
        results = api.search_services(args.argument)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for result in results:
                print(f"{result['id']}: {result['name']} [{result['category']}]")
    
    elif args.command == 'category':
        if not args.argument:
            # List all categories
            categories = api.get_all_categories()
            if args.json:
                print(json.dumps(categories, indent=2))
            else:
                for cat_name, cat_data in categories.items():
                    print(f"{cat_name}: {cat_data['description']}")
        else:
            # List services in category
            services = api.get_services_by_category(args.argument)
            if args.json:
                print(json.dumps(services))
            else:
                for service in services:
                    print(service)
    
    elif args.command == 'tag':
        if not args.argument:
            # List all tags
            tags = api.get_all_tags()
            if args.json:
                print(json.dumps(tags))
            else:
                for tag in sorted(tags):
                    print(tag)
        else:
            # List services with tag
            services = api.get_services_by_tag(args.argument)
            if args.json:
                print(json.dumps(services))
            else:
                for service in services:
                    print(service)