#!/bin/bash
# Install dependencies for PDF Auto-Extract skill

set -e

echo "========================================="
echo "PDF Auto-Extract - Dependency Installer"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Install pymupdf using Tsinghua mirror
echo "Installing pymupdf..."
pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user

echo ""
echo "========================================="
echo "✅ Installation Complete!"
echo "========================================="
echo ""
echo "You can now use the PDF Auto-Extract skill:"
echo "  python3 scripts/auto_extract.sh <pdf_file>"
echo ""
echo "For more information, see README.md"
