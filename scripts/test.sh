#!/bin/bash
# Test script for PDF Auto-Extract skill

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}PDF Auto-Extract - Test Suite${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Test 1: Check dependencies
echo -e "${YELLOW}Test 1: Checking dependencies...${NC}"
if python3 -c "import fitz" 2>/dev/null; then
    echo -e "${GREEN}✓ pymupdf is installed${NC}"
else
    echo -e "${RED}✗ pymupdf is not installed${NC}"
    echo "Please install it: pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user"
    exit 1
fi
echo ""

# Test 2: Check scripts
echo -e "${YELLOW}Test 2: Checking scripts...${NC}"
for script in extract_key_images.py generate_markdown.py auto_extract.sh install.sh utils.py; do
    if [ -f "scripts/$script" ]; then
        echo -e "${GREEN}✓ scripts/$script${NC}"
    else
        echo -e "${RED}✗ scripts/$script not found${NC}"
    fi
done
echo ""

# Test 3: Check files
echo -e "${YELLOW}Test 3: Checking documentation...${NC}"
for file in SKILL.md README.md QUICKSTART.md; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file${NC}"
    else
        echo -e "${RED}✗ $file not found${NC}"
    fi
done
echo ""

# Test 4: Test utils module
echo -e "${YELLOW}Test 4: Testing utils module...${NC}"
python3 scripts/utils.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ utils.py tests passed${NC}"
else
    echo -e "${RED}✗ utils.py tests failed${NC}"
fi
echo ""

# Test 5: Test PDF extraction (if test PDF exists)
echo -e "${YELLOW}Test 5: Testing PDF extraction...${NC}"
if [ -f "test.pdf" ]; then
    python3 scripts/extract_key_images.py test.pdf --output-dir test_output
    if [ -d "test_output" ]; then
        echo -e "${GREEN}✓ PDF extraction test passed${NC}"
        echo "  Extracted images: $(ls test_output/*.png 2>/dev/null | wc -l)"
    else
        echo -e "${RED}✗ PDF extraction test failed${NC}"
    fi
    rm -rf test_output
else
    echo -e "${YELLOW}⚠ No test PDF found. Skipping extraction test.${NC}"
fi
echo ""

# Test 6: Test markdown generation (if images exist)
echo -e "${YELLOW}Test 6: Testing markdown generation...${NC}"
if [ -d "extracted_images" ] && [ "$(ls -A extracted_images/*.png 2>/dev/null)" ]; then
    python3 scripts/generate_markdown.py test.pdf --images-dir extracted_images --output test_article.md
    if [ -f "test_article.md" ]; then
        echo -e "${GREEN}✓ Markdown generation test passed${NC}"
        echo "  Generated file: test_article.md"
        echo "  Image count: $(ls extracted_images/*.png | wc -l)"
    else
        echo -e "${RED}✗ Markdown generation test failed${NC}"
    fi
    rm -f test_article.md
else
    echo -e "${YELLOW}⚠ No images found. Skipping markdown test.${NC}"
fi
echo ""

echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}✅ All tests completed!${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""
echo "You can now use the skill:"
echo "  python3 scripts/auto_extract.sh <pdf_file>"
