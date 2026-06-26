# Quick Start Guide

Get started with PDF Auto-Extract in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user
```

This installs the PDF processing library using Tsinghua mirror for faster downloads.

## Step 2: Process Your PDF

```bash
python3 pdf-auto-extract/scripts/auto_extract.sh your_paper.pdf
```

That's it! The script will:
1. ✅ Install dependencies (if needed)
2. ✅ Extract key images from the PDF
3. ✅ Generate markdown with embedded images
4. ✅ Open the results for you

## Step 3: View Results

```bash
# View markdown file
cat article.md

# Open in browser
open article.md

# View extracted images
open extracted_images/
```

## What You Get

- **article.md** - Complete markdown file with:
  - Article summary
  - Key sections
  - Embedded images
  - Methodology and findings
  
- **extracted_images/** - Directory with:
  - All extracted images (figures, tables, charts)
  - Descriptive filenames
  - High quality screenshots

## Common Usage

### Process first 10 pages (default)
```bash
python3 scripts/auto_extract.sh paper.pdf
```

### Process specific pages (2-6)
```bash
python3 scripts/extract_key_images.py paper.pdf --page-range "2-6"
python3 scripts/generate_markdown.py paper.pdf --images-dir extracted_images
```

### Use region-based screenshot
```bash
python3 scripts/extract_key_images.py paper.pdf --screenshot-method region
```

### Custom output directory
```bash
python3 scripts/extract_key_images.py paper.pdf --output-dir my_images
python3 scripts/generate_markdown.py paper.pdf --images-dir my_images --output my_paper.md
```

## Tips

- **For best results**: Use full-page screenshot for complex diagrams
- **For simple figures**: Use region-based screenshot to avoid white space
- **Large PDFs**: Use `--page-range` to process only relevant pages
- **Quality control**: Review extracted images after processing

## Troubleshooting

### "pymupdf not installed"
```bash
pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user
```

### "No images detected"
- Ensure PDF contains visible images
- Check image sizes (minimum 500x500 pixels)
- Try region-based screenshot method

### Screenshot not working
- Ensure Preview is installed: `open -a Preview`
- Check macOS screenshot permissions

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/](examples/) for more usage examples
- Customize the scripts to fit your needs

## Need Help?

- Check the [README.md](README.md) for detailed troubleshooting
- Review the [SKILL.md](SKILL.md) for skill-specific information
- Consult pymupdf documentation: https://pymupdf.readthedocs.io/
