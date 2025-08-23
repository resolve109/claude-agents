#!/usr/bin/env python3
"""
AWS Documentation PDF to Text Converter
Uses various methods to convert AWS documentation PDFs to searchable text files
"""

import json
import os
import sys
import argparse
import requests
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import hashlib

# Base directories
BASE_DIR = Path("/mnt/e/github/agents/claude-agents/.claude/data/shared/references/aws-docs")
MASTER_INDEX = BASE_DIR / "master-index.json"
PDF_DIR = BASE_DIR / "pdfs"
TEXT_DIR = BASE_DIR / "text"
CACHE_DIR = BASE_DIR / "cache"

# Create directories if they don't exist
for dir_path in [PDF_DIR, TEXT_DIR, CACHE_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

def load_master_index() -> Dict:
    """Load the master index of AWS services"""
    with open(MASTER_INDEX, 'r') as f:
        return json.load(f)

def get_file_hash(file_path: Path) -> str:
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def download_pdf(service: str, pdf_url: str) -> Optional[Path]:
    """Download PDF for a service"""
    pdf_path = PDF_DIR / f"{service}.pdf"
    
    # Check if already downloaded
    if pdf_path.exists():
        print(f"✓ PDF already exists: {pdf_path}")
        return pdf_path
    
    print(f"⬇ Downloading PDF for {service}...")
    print(f"  URL: {pdf_url}")
    
    try:
        response = requests.get(pdf_url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Write PDF in chunks
        with open(pdf_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        file_size = pdf_path.stat().st_size / (1024 * 1024)  # Convert to MB
        print(f"✓ Downloaded {service}.pdf ({file_size:.2f} MB)")
        return pdf_path
        
    except requests.RequestException as e:
        print(f"✗ Failed to download {service}: {e}")
        return None

def convert_with_pdfplumber(pdf_path: Path, text_path: Path) -> bool:
    """Convert PDF using pdfplumber (Python library)"""
    try:
        import pdfplumber
        
        print("  Using pdfplumber...")
        text = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text.append(f"--- Page {i} ---\n{page_text}")
        
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(text))
        
        return True
    except ImportError:
        print("  pdfplumber not available (install with: pip install pdfplumber)")
        return False
    except Exception as e:
        print(f"  pdfplumber failed: {e}")
        return False

def convert_with_pypdf2(pdf_path: Path, text_path: Path) -> bool:
    """Convert PDF using PyPDF2"""
    try:
        import PyPDF2
        
        print("  Using PyPDF2...")
        text = []
        
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text.append(f"--- Page {i} ---\n{page_text}")
        
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(text))
        
        return True
    except ImportError:
        print("  PyPDF2 not available (install with: pip install PyPDF2)")
        return False
    except Exception as e:
        print(f"  PyPDF2 failed: {e}")
        return False

def convert_with_pdftotext(pdf_path: Path, text_path: Path) -> bool:
    """Convert PDF using pdftotext command-line tool"""
    try:
        print("  Using pdftotext...")
        result = subprocess.run(
            ['pdftotext', str(pdf_path), str(text_path)],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("  pdftotext not available (install with: apt-get install poppler-utils)")
        return False
    except Exception as e:
        print(f"  pdftotext failed: {e}")
        return False

def convert_with_mcp_mdconvert(pdf_path: Path, text_path: Path) -> bool:
    """Try to use MCP mdconvert server if available"""
    try:
        print("  Checking for MCP mdconvert server...")
        # This would require the MCP server to be running
        # For now, we'll just check if it's configured
        mcp_config_path = Path("/mnt/e/github/agents/claude-agents/.claude/mcp/config.json")
        if mcp_config_path.exists():
            with open(mcp_config_path, 'r') as f:
                config = json.load(f)
                if 'mdconvert' in config.get('mcpServers', {}):
                    print("  MCP mdconvert server is configured but requires manual invocation")
                    return False
        return False
    except Exception as e:
        print(f"  MCP check failed: {e}")
        return False

def convert_pdf_to_text(service: str, pdf_path: Path) -> Optional[Path]:
    """Convert PDF to text using available methods"""
    text_path = TEXT_DIR / f"{service}.txt"
    
    # Check if already converted
    if text_path.exists():
        print(f"✓ Text file already exists: {text_path}")
        return text_path
    
    print(f"🔄 Converting {service}.pdf to text...")
    
    # Try different conversion methods in order of preference
    converters = [
        ("pdfplumber", convert_with_pdfplumber),
        ("pdftotext", convert_with_pdftotext),
        ("PyPDF2", convert_with_pypdf2),
        ("MCP mdconvert", convert_with_mcp_mdconvert)
    ]
    
    for name, converter in converters:
        if converter(pdf_path, text_path):
            if text_path.exists():
                file_size = text_path.stat().st_size / 1024  # Convert to KB
                print(f"✓ Converted to text using {name} ({file_size:.2f} KB)")
                return text_path
    
    print(f"✗ Failed to convert {service}.pdf to text")
    return None

def create_service_metadata(service: str, service_info: Dict) -> Path:
    """Create metadata file for a service"""
    metadata_path = TEXT_DIR / f"{service}_metadata.json"
    
    metadata = {
        "service": service,
        "name": service_info["name"],
        "category": service_info["category"],
        "description": service_info["description"],
        "pdf_url": service_info["pdf_url"],
        "pdf_downloaded": (PDF_DIR / f"{service}.pdf").exists(),
        "text_converted": (TEXT_DIR / f"{service}.txt").exists(),
        "last_updated": str(Path(PDF_DIR / f"{service}.pdf").stat().st_mtime) if (PDF_DIR / f"{service}.pdf").exists() else None
    }
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return metadata_path

def process_service(service: str, download: bool = True, convert: bool = True) -> bool:
    """Process a single service: download and/or convert"""
    index = load_master_index()
    
    if service not in index["services"]:
        print(f"✗ Service '{service}' not found")
        return False
    
    service_info = index["services"][service]
    print(f"\n📚 Processing {service_info['name']} ({service})")
    print(f"  Category: {service_info['category']}")
    print(f"  Description: {service_info['description']}")
    
    pdf_path = None
    if download:
        pdf_path = download_pdf(service, service_info["pdf_url"])
        if not pdf_path:
            return False
    else:
        pdf_path = PDF_DIR / f"{service}.pdf"
        if not pdf_path.exists():
            print(f"✗ PDF not found: {pdf_path}")
            return False
    
    text_path = None
    if convert and pdf_path:
        text_path = convert_pdf_to_text(service, pdf_path)
    
    # Create metadata
    metadata_path = create_service_metadata(service, service_info)
    print(f"✓ Metadata saved: {metadata_path}")
    
    return bool(pdf_path and (text_path if convert else True))

def process_category(category: str, download: bool = True, convert: bool = True) -> None:
    """Process all services in a category"""
    index = load_master_index()
    
    if category not in index["categories"]:
        print(f"✗ Category '{category}' not found")
        print("Available categories:", ", ".join(index["categories"].keys()))
        return
    
    cat_info = index["categories"][category]
    services = cat_info["services"]
    
    print(f"\n📁 Processing category: {cat_info['name']}")
    print(f"  Services: {len(services)}")
    
    success_count = 0
    for service in services:
        if process_service(service, download, convert):
            success_count += 1
    
    print(f"\n✅ Processed {success_count}/{len(services)} services successfully")

def list_status() -> None:
    """List the status of all services"""
    index = load_master_index()
    
    print("\n📊 AWS Documentation Status")
    print("=" * 50)
    
    total_services = len(index["services"])
    downloaded = 0
    converted = 0
    
    for service, info in index["services"].items():
        pdf_exists = (PDF_DIR / f"{service}.pdf").exists()
        text_exists = (TEXT_DIR / f"{service}.txt").exists()
        
        if pdf_exists:
            downloaded += 1
        if text_exists:
            converted += 1
        
        status = []
        if pdf_exists:
            status.append("PDF ✓")
        if text_exists:
            status.append("TXT ✓")
        
        if not status:
            status.append("Not downloaded")
        
        print(f"{service:20} {info['name']:30} [{' | '.join(status)}]")
    
    print("\n" + "=" * 50)
    print(f"Total services: {total_services}")
    print(f"PDFs downloaded: {downloaded}/{total_services} ({downloaded*100//total_services}%)")
    print(f"Texts converted: {converted}/{total_services} ({converted*100//total_services}%)")

def main():
    parser = argparse.ArgumentParser(description="AWS Documentation PDF to Text Converter")
    parser.add_argument("command", choices=["service", "category", "all", "status"],
                      help="Command to execute")
    parser.add_argument("target", nargs="?", help="Service or category name")
    parser.add_argument("--download-only", action="store_true",
                      help="Only download PDFs, don't convert")
    parser.add_argument("--convert-only", action="store_true",
                      help="Only convert existing PDFs to text")
    
    args = parser.parse_args()
    
    if args.command == "status":
        list_status()
    elif args.command == "service":
        if not args.target:
            print("Error: Service name required")
            sys.exit(1)
        download = not args.convert_only
        convert = not args.download_only
        success = process_service(args.target, download, convert)
        sys.exit(0 if success else 1)
    elif args.command == "category":
        if not args.target:
            print("Error: Category name required")
            sys.exit(1)
        download = not args.convert_only
        convert = not args.download_only
        process_category(args.target, download, convert)
    elif args.command == "all":
        index = load_master_index()
        download = not args.convert_only
        convert = not args.download_only
        
        for category in index["categories"]:
            process_category(category, download, convert)

if __name__ == "__main__":
    main()