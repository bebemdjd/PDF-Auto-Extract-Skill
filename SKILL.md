---
name: pdf-auto-extract
description: Automatically extract key experimental images from PDF academic papers and generate markdown with embedded images using pymupdf and macOS screenshot tools. Perfect for research papers requiring: (1) Automatic detection of figures/tables/charts, (2) Full-page or region screenshot of key images, (3) Smart filtering of non-relevant images, (4) Markdown generation with embedded images and article summary, (5) Complete skill package ready to use
---

# PDF Auto-Extract

## Overview

Intelligent PDF processing skill that automatically extracts key experimental images (figures, tables, charts, diagrams) from academic papers and generates a comprehensive markdown file with embedded images. Uses pymupdf for intelligent image detection and macOS screenshot tools for capturing key images.

## Key Features

- ✅ **Automatic Image Detection**: Identifies figures, tables, charts, and diagrams using image analysis
- ✅ **Smart Filtering**: Filters out title pages, abstract, references, and non-visual content
- ✅ **Full Automation**: Complete workflow from PDF to markdown with embedded images
- ✅ **Flexible Screenshot Options**: Full-page or region-based screenshot selection
- ✅ **Article Summary**: Auto-generates article summary and structure
- ✅ **Ready-to-Use Package**: Complete skill package with all necessary scripts

## Workflow

### Step 1: Install Dependencies

```bash
pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user
```

### Step 2: Process PDF

```bash
python3 pdf-auto-extract/scripts/extract_key_images.py <pdf_file>
```

Or use the automated script:
```bash
python3 pdf-auto-extract/scripts/auto_extract.sh <pdf_file>
```

### Step 3: Generate Markdown

```bash
python3 pdf-auto-extract/scripts/generate_markdown.py <pdf_file>
```

## Resources

### scripts/extract_key_images.py

Main script for intelligent image extraction and screenshot capture.

### scripts/generate_markdown.py

Generate markdown file with embedded images.

### scripts/auto_extract.sh

Automated workflow script.

### scripts/complete_screenshot_guide.sh

Interactive screenshot guide.

## Usage Examples

```bash
# Full automation with full-page screenshots
python3 scripts/extract_key_images.py paper.pdf --screenshot-method full

# Region-based screenshot for selective cropping
python3 scripts/extract_key_images.py paper.pdf --screenshot-method region

# Process specific page range
python3 scripts/extract_key_images.py paper.pdf --page-range "2-6"

# Custom output directory
python3 scripts/extract_key_images.py paper.pdf --output-dir my_images
```

## Output Structure

```
pdf-auto-extract/
├── SKILL.md                      # This skill file
├── README.md                     # Detailed documentation
├── QUICKSTART.md                 # Quick start guide
├── scripts/
│   ├── extract_key_images.py    # Main extraction script
│   ├── generate_markdown.py     # Markdown generator
│   ├── auto_extract.sh          # Automated workflow
│   ├── complete_screenshot_guide.sh  # Interactive guide
│   └── utils.py                 # Helper functions
└── examples/
    └── example_usage.md          # Usage examples
```

## Troubleshooting

### pymupdf installation fails
```bash
pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user
```

### No images detected
- Ensure PDF contains visible images
- Check image sizes (minimum 500x500 pixels)
- Try region-based screenshot method

### Screenshot not working
- Ensure Preview is installed: `open -a Preview`
- Check macOS screenshot permissions
- Try manual screenshot with Cmd+Shift+4

## Version History

- **v1.0** (2025-06): Initial release with full automation capabilities
