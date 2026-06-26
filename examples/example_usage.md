# Usage Examples

This file contains practical examples of how to use the PDF Auto-Extract skill.

## Example 1: Basic Academic Paper Processing

**Scenario**: You have a research paper in PDF format and want to extract all figures and generate a markdown summary.

```bash
# 1. Navigate to the skill directory
cd pdf-auto-extract

# 2. Install dependencies (one-time)
pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user

# 3. Process the PDF
python3 scripts/auto_extract.sh /path/to/your/paper.pdf
```

**Result**:
- extracted_images/ folder with all extracted images
- article.md with article summary and embedded images

## Example 2: Process Specific Page Range

**Scenario**: You only need figures from pages 2-6 (methodology and results sections).

```bash
python3 scripts/extract_key_images.py /path/to/your/paper.pdf --page-range "2-6" --output-dir extracted_images
python3 scripts/generate_markdown.py /path/to/your/paper.pdf --images-dir extracted_images
```

**Why this is useful**:
- Faster processing (only 5 pages instead of 10)
- Fewer irrelevant images (title page, references, etc.)
- More focused on key content

## Example 3: Region-Based Screenshot

**Scenario**: You want to capture only specific regions (e.g., single figures) rather than full pages.

```bash
python3 scripts/extract_key_images.py /path/to/your/paper.pdf --screenshot-method region
```

**How it works**:
- Opens PDF in Preview
- Uses macOS screenshot tool (Cmd+Shift+4)
- Allows you to select specific areas
- Captures only the selected region

**Pros**:
- Avoids capturing white space
- Smaller image files
- More precise selection

**Cons**:
- Requires manual interaction
- Slower for multiple images

## Example 4: Custom Output Directory and Filename

**Scenario**: You want to organize multiple papers in a structured way.

```bash
# Create a project directory
mkdir -p research_papers/paper1

# Extract images for paper 1
python3 scripts/extract_key_images.py paper1.pdf \
    --output-dir research_papers/paper1/extracted_images

# Generate markdown for paper 1
python3 scripts/generate_markdown.py paper1.pdf \
    --images-dir research_papers/paper1/extracted_images \
    --output research_papers/paper1/article.md
```

**Result**:
```
research_papers/
└── paper1/
    ├── article.md
    └── extracted_images/
        ├── page1_img1_figure.png
        ├── page2_img2_table.png
        └── ...
```

## Example 5: Batch Processing Multiple Papers

**Scenario**: You have 10 research papers and want to process them all.

```bash
# Create a batch script
for paper in papers/*.pdf; do
    echo "Processing $paper..."
    python3 scripts/auto_extract.sh "$paper"
done
```

**Alternative**: Use a loop in your shell:

```bash
for paper in papers/*.pdf; do
    echo "Processing $paper..."
    python3 scripts/auto_extract.sh "$paper"
done
```

## Example 6: Generate HTML Output

**Scenario**: You want a more visually appealing output with CSS styling.

```bash
# First, extract images
python3 scripts/extract_key_images.py paper.pdf --output-dir extracted_images

# Then, generate markdown
python3 scripts/generate_markdown.py paper.pdf --images-dir extracted_images --output article.md

# Convert to HTML (requires markdown library)
pip3 install markdown --user
python3 -c "
import markdown
with open('article.md', 'r') as f:
    content = f.read()
html = markdown.markdown(content)
with open('article.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        img { max-width: 100%; }
    </style>
</head>
<body>
{html}
</body>
</html>''')
"
```

## Example 7: Extract Images Only (No Markdown)

**Scenario**: You only want the images for further processing.

```bash
# Extract images only
python3 scripts/extract_key_images.py paper.pdf --output-dir extracted_images
```

**Use case**:
- You want to manually select which images to use
- You want to process images with other tools
- You want to create a custom presentation

## Example 8: Generate PDF from Markdown

**Scenario**: You want to convert the markdown file to PDF.

```bash
# Convert markdown to PDF
pip3 install markdown --user
python3 -c "
import markdown
import pdfkit

with open('article.md', 'r') as f:
    content = f.read()
html = markdown.markdown(content)

pdfkit.from_string(html, 'article.pdf')
"
```

## Example 9: Integrate with LaTeX

**Scenario**: You want to include the extracted images in a LaTeX document.

```bash
# Extract images
python3 scripts/extract_key_images.py paper.pdf --output-dir extracted_images

# Generate markdown
python3 scripts/generate_markdown.py paper.pdf --images-dir extracted_images --output article.md

# Convert to LaTeX (requires markdown to latex converter)
pip3 install markdown2latex --user
python3 -c "
import markdown2latex
from pathlib import Path

md_file = Path('article.md')
latex = markdown2latex.convert(md_file.read_text())

latex_file = Path('article.tex')
latex_file.write_text(latex)
"
```

## Example 10: Automated Pipeline

**Scenario**: You want to create an automated pipeline for research paper processing.

```bash
# Create a pipeline script
mkdir -p pipeline_output

# Process a paper with automated workflow
python3 scripts/auto_extract.sh paper.pdf --output-dir pipeline_output

# View results
open pipeline_output/
```

## Best Practices

1. Always check extracted images - Review them to ensure quality
2. Use appropriate page ranges - Avoid processing unnecessary pages
3. Organize outputs - Use custom directories for different projects
4. Backup original PDFs - Keep the original files for reference
5. Document your workflow - Keep track of parameters used

## Troubleshooting Examples

### No images extracted
```bash
# Check if PDF has images
pdfinfo paper.pdf | grep Pages

# Try with larger minimum size
python3 scripts/extract_key_images.py paper.pdf --min-size 800 800
```

### Images too large
```bash
# Use region-based screenshot
python3 scripts/extract_key_images.py paper.pdf --screenshot-method region
```

### Markdown generation fails
```bash
# Check if images directory exists
ls -la extracted_images/

# Verify images are in the correct format
file extracted_images/*.png
```

## Advanced Tips

1. Combine with other tools: Use extracted images in other analysis tools
2. Customize scripts: Modify the Python scripts to fit your needs
3. Batch processing: Process multiple papers efficiently
4. Automation: Integrate into your research workflow
5. Quality control: Add validation steps for image quality

For more information, see the README.md and SKILL.md.

