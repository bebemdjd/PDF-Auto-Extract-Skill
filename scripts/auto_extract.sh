#!/bin/bash
# Automated PDF extraction workflow

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if PDF file is provided
if [ $# -eq 0 ]; then
    echo "Error: No PDF file provided"
    echo "Usage: $0 <pdf_file> [options]"
    echo ""
    echo "Options:"
    echo "  --page-range RANGE    Process specific page range (e.g., '2-6')"
    echo "  --output-dir DIR      Custom output directory"
    echo ""
    exit 1
fi

PDF_FILE="$1"
shift

# Parse options
PAGE_RANGE=""
OUTPUT_DIR="extracted_images"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --page-range)
            PAGE_RANGE="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Check if PDF exists
if [ ! -f "$PDF_FILE" ]; then
    echo "Error: PDF file not found: $PDF_FILE"
    exit 1
fi

echo "========================================="
echo "PDF Auto-Extract Workflow"
echo "========================================="
echo ""
echo "PDF File: $PDF_FILE"
echo "Output Directory: $OUTPUT_DIR"
echo "Page Range: ${PAGE_RANGE:-All pages (first 10)}"
echo ""

# Step 1: Install dependencies
echo "Step 1: Installing dependencies..."
pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user --quiet
echo "✓ Dependencies installed"
echo ""

# Step 2: Extract images
echo "Step 2: Extracting key images..."
if [ -n "$PAGE_RANGE" ]; then
    python3 scripts/extract_key_images.py "$PDF_FILE" --output-dir "$OUTPUT_DIR" --page-range "$PAGE_RANGE"
else
    python3 scripts/extract_key_images.py "$PDF_FILE" --output-dir "$OUTPUT_DIR"
fi
echo ""

# Step 3: Generate markdown
echo "Step 3: Generating markdown file..."
python3 scripts/generate_markdown.py "$PDF_FILE" --images-dir "$OUTPUT_DIR"
echo ""

# Step 4: Open results
echo "Step 4: Opening results..."
echo "✓ Extraction complete!"
echo ""
echo "Files generated:"
echo "  - Markdown file: article.md"
echo "  - Extracted images: $OUTPUT_DIR/"
echo ""
echo "To view the markdown file:"
echo "  cat article.md"
echo ""
echo "To open the markdown in a browser:"
echo "  open article.md"
echo ""
echo "To view extracted images:"
echo "  open $OUTPUT_DIR/"
echo ""

# Exit successfully
echo "========================================="
echo "✅ Workflow Complete!"
echo "========================================="

