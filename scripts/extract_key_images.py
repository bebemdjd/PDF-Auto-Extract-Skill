#!/usr/bin/env python3
"""
PDF Key Image Extractor - Automatic detection and extraction of key experimental images

This script automatically detects and extracts key images (figures, tables, charts) from PDF papers,
captures screenshots using macOS tools, and prepares them for markdown generation.
"""

import sys
import os
import argparse
import subprocess
import json
from pathlib import Path
from datetime import datetime

try:
    import fitz  # pymupdf
except ImportError:
    print("Error: pymupdf is not installed")
    print("Please install it using:")
    print("  pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user")
    sys.exit(1)


class PDFImageExtractor:
    """Extract key images from PDF with intelligent detection."""
    
    def __init__(self, pdf_path, output_dir="extracted_images", 
                 min_size=(500, 500), max_pages=10, screenshot_method="full"):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.min_size = min_size
        self.max_pages = max_pages
        self.screenshot_method = screenshot_method
        self.extracted_images = []
        self.doc = None
        
    def open_pdf(self):
        """Open the PDF file."""
        print(f"Opening PDF: {self.pdf_path}")
        self.doc = fitz.open(self.pdf_path)
        print(f"PDF loaded: {len(self.doc)} pages")
        print()
        
    def close_pdf(self):
        """Close the PDF file."""
        if self.doc:
            self.doc.close()
            
    def is_relevant_page(self, page_num):
        """Check if a page contains relevant content."""
        page = self.doc[page_num]
        text = page.get_text()
        
        # Skip these pages
        skip_keywords = [
            'abstract', 'references', 'bibliography', 'acknowledgments',
            'author biography', 'author information', 'keywords', 'doi',
            'copyright', 'publisher', 'conference', 'conference proceedings',
            'conference logo', 'table of contents', 'index', 'contents'
        ]
        
        text_lower = text.lower()
        
        for keyword in skip_keywords:
            if keyword in text_lower:
                return False
        
        # Check if page has significant content
        if len(text.strip()) < 100:
            return False
            
        return True
    
    def detect_image_type(self, image_rect, page_num):
        """Detect type of image based on its location and properties."""
        x0, y0, x1, y1 = image_rect
        
        # Check if image is in a typical figure location (middle of page)
        page_height = self.doc[page_num].rect.height
        if y0 > page_height * 0.3 and y1 < page_height * 0.9:
            return "figure"
        
        # Check if image is near bottom (tables)
        if y1 > page_height * 0.8:
            return "table"
            
        return "image"
    
    def extract_images_from_page(self, page_num):
        """Extract images from a single page."""
        page = self.doc[page_num]
        image_list = page.get_images(full=True)
        
        extracted = []
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = self.doc.extract_image(xref)
            
            # Check image size
            img_width = base_image["width"]
            img_height = base_image["height"]
            
            if img_width < self.min_size[0] or img_height < self.min_size[1]:
                continue
            
            # Get image position
            try:
                img_rect = page.get_image_rects(xref)
                if img_rect:
                    img_rect = img_rect[0]
                else:
                    # If no position info, use full page
                    img_rect = page.rect
            except:
                img_rect = page.rect
            
            # Detect image type
            img_type = self.detect_image_type(img_rect, page_num)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"page{page_num + 1}_img{img_index + 1}_{img_type}.{base_image['ext']}"
            
            extracted.append({
                'page': page_num + 1,
                'xref': xref,
                'filename': filename,
                'width': img_width,
                'height': img_height,
                'type': img_type,
                'rect': img_rect
            })
        
        return extracted
    
    def capture_screenshot(self, page_num, filename, rect=None):
        """Capture screenshot using macOS tools."""
        page = self.doc[page_num]
        
        if self.screenshot_method == "full":
            # Full page screenshot
            rect = page.rect
        elif rect:
            # Region screenshot
            rect = rect
        else:
            # Default to full page
            rect = page.rect
        
        # Create screenshot command
        cmd = [
            "screencapture", "-R",
            f"{int(rect.x0)},{int(rect.y0)},{int(rect.x1-rect.x0)},{int(rect.y1-rect.y0)}",
            str(self.output_dir / filename)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✓ Screenshot captured: {filename}")
                return True
            else:
                print(f"  ✗ Screenshot failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"  ✗ Screenshot error: {e}")
            return False
    
    def process(self):
        """Process the PDF and extract key images."""
        if not self.pdf_path.exists():
            print(f"Error: PDF file not found: {self.pdf_path}")
            return False
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {self.output_dir}")
        print()
        
        # Open PDF
        self.open_pdf()
        
        # Process pages
        total_pages = min(len(self.doc), self.max_pages)
        print(f"Processing pages 1-{total_pages}...")
        print()
        
        processed_count = 0
        
        for page_num in range(total_pages):
            if not self.is_relevant_page(page_num):
                continue
            
            print(f"Processing page {page_num + 1}...")
            
            # Extract images from page
            images = self.extract_images_from_page(page_num)
            
            if images:
                print(f"  Found {len(images)} image(s)")
                for img in images:
                    print(f"    - {img['filename']} ({img['width']}x{img['height']}, {img['type']})")
                    
                    # Capture screenshot
                    if self.capture_screenshot(page_num, img['filename'], img['rect']):
                        self.extracted_images.append(img)
                        processed_count += 1
            else:
                print(f"  No images found on this page")
            
            print()
        
        # Close PDF
        self.close_pdf()
        
        # Summary
        print("=" * 60)
        print(f"✅ Extraction Complete!")
        print("=" * 60)
        print(f"Total pages processed: {total_pages}")
        print(f"Images extracted: {processed_count}")
        print(f"Images saved to: {self.output_dir}")
        print()
        
        return processed_count > 0


def main():
    parser = argparse.ArgumentParser(
        description="Extract key images from PDF papers automatically"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output-dir", "-o", default="extracted_images",
                       help="Output directory for extracted images")
    parser.add_argument("--min-size", nargs=2, type=int, default=[500, 500],
                       help="Minimum image size (width height)")
    parser.add_argument("--max-pages", type=int, default=10,
                       help="Maximum pages to process")
    parser.add_argument("--screenshot-method", choices=["full", "region"],
                       default="full",
                       help="Screenshot method: 'full' (full page) or 'region'")
    
    args = parser.parse_args()
    
    extractor = PDFImageExtractor(
        pdf_path=args.pdf_path,
        output_dir=args.output_dir,
        min_size=tuple(args.min_size),
        max_pages=args.max_pages,
        screenshot_method=args.screenshot_method
    )
    
    success = extractor.process()
    
    if not success:
        print("No images were extracted. Check if the PDF contains images.")
        sys.exit(1)


if __name__ == "__main__":
    main()
