#!/bin/bash

# AWS Documentation Lookup Script
# Usage: ./aws-docs-lookup.sh [service|category|search] [query]

DOCS_DIR="/mnt/e/github/agents/claude-agents/.claude/data/shared/references/aws-docs"
MASTER_INDEX="$DOCS_DIR/master-index.json"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
show_usage() {
    echo "AWS Documentation Lookup Tool"
    echo "=============================="
    echo ""
    echo "Usage: $0 [command] [query]"
    echo ""
    echo "Commands:"
    echo "  service <name>     - Get documentation URL for a specific service"
    echo "  category <name>    - List all services in a category"
    echo "  search <term>      - Search for services matching a term"
    echo "  list-categories    - List all available categories"
    echo "  list-services      - List all available services"
    echo "  download <service> - Download PDF for a service"
    echo "  convert <service>  - Convert PDF to text (requires pdf2txt)"
    echo ""
    echo "Examples:"
    echo "  $0 service ec2"
    echo "  $0 category networking"
    echo "  $0 search lambda"
    echo "  $0 download s3"
}

# Function to get service info
get_service() {
    local service=$1
    if [ -z "$service" ]; then
        echo -e "${RED}Error: Service name required${NC}"
        return 1
    fi
    
    local result=$(jq -r ".services.\"$service\" // empty" "$MASTER_INDEX")
    
    if [ -z "$result" ]; then
        echo -e "${RED}Service '$service' not found${NC}"
        echo "Use '$0 list-services' to see available services"
        return 1
    fi
    
    echo -e "${GREEN}Service: ${NC}$(echo "$result" | jq -r '.name')"
    echo -e "${BLUE}Description: ${NC}$(echo "$result" | jq -r '.description')"
    echo -e "${YELLOW}Category: ${NC}$(echo "$result" | jq -r '.category')"
    echo -e "${BLUE}PDF URL: ${NC}$(echo "$result" | jq -r '.pdf_url')"
}

# Function to list services in a category
get_category() {
    local category=$1
    if [ -z "$category" ]; then
        echo -e "${RED}Error: Category name required${NC}"
        return 1
    fi
    
    local cat_info=$(jq -r ".categories.\"$category\" // empty" "$MASTER_INDEX")
    
    if [ -z "$cat_info" ]; then
        echo -e "${RED}Category '$category' not found${NC}"
        echo "Use '$0 list-categories' to see available categories"
        return 1
    fi
    
    echo -e "${GREEN}Category: ${NC}$(echo "$cat_info" | jq -r '.name')"
    echo -e "${BLUE}Services in this category:${NC}"
    echo ""
    
    local services=$(echo "$cat_info" | jq -r '.services[]')
    for service in $services; do
        local service_info=$(jq -r ".services.\"$service\"" "$MASTER_INDEX")
        local name=$(echo "$service_info" | jq -r '.name')
        local desc=$(echo "$service_info" | jq -r '.description')
        echo "  • $name ($service)"
        echo "    $desc"
        echo ""
    done
}

# Function to search for services
search_services() {
    local term=$1
    if [ -z "$term" ]; then
        echo -e "${RED}Error: Search term required${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Searching for: ${NC}$term"
    echo ""
    
    # Search in service names and descriptions
    local results=$(jq -r ".services | to_entries[] | select(.key | contains(\"$term\")) or select(.value.name | ascii_downcase | contains(\"${term,,}\")) or select(.value.description | ascii_downcase | contains(\"${term,,}\"))" "$MASTER_INDEX")
    
    if [ -z "$results" ]; then
        echo -e "${YELLOW}No services found matching '$term'${NC}"
        return 1
    fi
    
    echo "$results" | jq -r '"  • \(.value.name) (\(.key))\n    \(.value.description)\n    Category: \(.value.category)\n"'
}

# Function to list all categories
list_categories() {
    echo -e "${GREEN}Available Categories:${NC}"
    echo ""
    jq -r '.categories | to_entries[] | "  • \(.value.name) (\(.key))\n    Services: \(.value.services | join(", "))\n"' "$MASTER_INDEX"
}

# Function to list all services
list_services() {
    echo -e "${GREEN}Available AWS Services:${NC}"
    echo ""
    jq -r '.services | to_entries[] | "  • \(.value.name) (\(.key)) - \(.value.category)"' "$MASTER_INDEX" | sort
}

# Function to download PDF
download_pdf() {
    local service=$1
    if [ -z "$service" ]; then
        echo -e "${RED}Error: Service name required${NC}"
        return 1
    fi
    
    local pdf_url=$(jq -r ".services.\"$service\".pdf_url // empty" "$MASTER_INDEX")
    
    if [ -z "$pdf_url" ]; then
        echo -e "${RED}Service '$service' not found${NC}"
        return 1
    fi
    
    local pdf_dir="$DOCS_DIR/pdfs"
    mkdir -p "$pdf_dir"
    
    local pdf_file="$pdf_dir/${service}.pdf"
    
    echo -e "${GREEN}Downloading PDF for $service...${NC}"
    echo "URL: $pdf_url"
    echo "Destination: $pdf_file"
    
    if command -v wget &> /dev/null; then
        wget -O "$pdf_file" "$pdf_url"
    elif command -v curl &> /dev/null; then
        curl -L -o "$pdf_file" "$pdf_url"
    else
        echo -e "${RED}Error: Neither wget nor curl is installed${NC}"
        return 1
    fi
    
    if [ -f "$pdf_file" ]; then
        echo -e "${GREEN}PDF downloaded successfully: $pdf_file${NC}"
    else
        echo -e "${RED}Failed to download PDF${NC}"
        return 1
    fi
}

# Function to convert PDF to text
convert_to_text() {
    local service=$1
    if [ -z "$service" ]; then
        echo -e "${RED}Error: Service name required${NC}"
        return 1
    fi
    
    local pdf_file="$DOCS_DIR/pdfs/${service}.pdf"
    local text_dir="$DOCS_DIR/text"
    mkdir -p "$text_dir"
    
    local text_file="$text_dir/${service}.txt"
    
    if [ ! -f "$pdf_file" ]; then
        echo -e "${YELLOW}PDF not found. Downloading first...${NC}"
        download_pdf "$service"
    fi
    
    if [ ! -f "$pdf_file" ]; then
        echo -e "${RED}Failed to get PDF file${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Converting PDF to text for $service...${NC}"
    
    # Try different PDF to text converters
    if command -v pdftotext &> /dev/null; then
        pdftotext "$pdf_file" "$text_file"
    elif command -v pdf2txt &> /dev/null; then
        pdf2txt -o "$text_file" "$pdf_file"
    elif command -v python3 &> /dev/null && python3 -c "import PyPDF2" 2>/dev/null; then
        python3 -c "
import PyPDF2
import sys

with open('$pdf_file', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    
with open('$text_file', 'w', encoding='utf-8') as output:
    output.write(text)
"
    else
        echo -e "${RED}Error: No PDF to text converter available${NC}"
        echo "Please install one of: pdftotext, pdf2txt, or python3 with PyPDF2"
        return 1
    fi
    
    if [ -f "$text_file" ]; then
        echo -e "${GREEN}Text file created successfully: $text_file${NC}"
        echo "File size: $(du -h "$text_file" | cut -f1)"
    else
        echo -e "${RED}Failed to convert PDF to text${NC}"
        return 1
    fi
}

# Main command handler
case "$1" in
    service)
        get_service "$2"
        ;;
    category)
        get_category "$2"
        ;;
    search)
        search_services "$2"
        ;;
    list-categories)
        list_categories
        ;;
    list-services)
        list_services
        ;;
    download)
        download_pdf "$2"
        ;;
    convert)
        convert_to_text "$2"
        ;;
    *)
        show_usage
        ;;
esac