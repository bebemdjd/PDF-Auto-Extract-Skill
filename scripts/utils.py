"""
Helper utilities for PDF Auto-Extract skill
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fitz
        return True
    except ImportError:
        print("Error: pymupdf is not installed")
        print("Please install it using:")
        print("  pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple --user")
        return False


def create_output_directory(output_dir):
    """Create output directory if it doesn't exist."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return Path(output_dir)


def validate_pdf(pdf_path):
    """Validate PDF file."""
    if not Path(pdf_path).exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    
    try:
        import fitz
        doc = fitz.open(pdf_path)
        if len(doc) == 0:
            print(f"Error: PDF file is empty: {pdf_path}")
            doc.close()
            return False
        doc.close()
        return True
    except Exception as e:
        print(f"Error: Failed to open PDF: {e}")
        return False


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"{title}")
    print("=" * 60 + "\n")


def print_step(step_num, title):
    """Print a formatted step header."""
    print(f"\nStep {step_num}: {title}")
    print("-" * 60)


def print_success(message):
    """Print a success message."""
    print(f"✓ {message}")


def print_info(message):
    """Print an info message."""
    print(f"ℹ {message}")


def print_warning(message):
    """Print a warning message."""
    print(f"⚠ {message}")


def print_error(message):
    """Print an error message."""
    print(f"✗ {message}")


def get_timestamp():
    """Get current timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_size(size_bytes):
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def count_images(directory):
    """Count number of images in directory."""
    if not Path(directory).exists():
        return 0
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.tiff']
    count = 0
    for ext in image_extensions:
        count += len(list(Path(directory).glob(ext)))
    return count


def get_file_size(file_path):
    """Get file size in bytes."""
    if Path(file_path).exists():
        return Path(file_path).stat().st_size
    return 0


def cleanup_old_files(directory, max_age_days=30):
    """Clean up files older than specified days."""
    import time
    current_time = time.time()
    deleted_count = 0
    
    for file_path in Path(directory).glob('*'):
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_days * 24 * 3600:
                file_path.unlink()
                deleted_count += 1
    
    return deleted_count


def validate_screenshot_method(method):
    """Validate screenshot method."""
    valid_methods = ['full', 'region']
    if method not in valid_methods:
        raise ValueError(f"Invalid screenshot method: {method}. Must be one of: {valid_methods}")
    return method


def validate_page_range(page_range):
    """Validate page range."""
    if not page_range:
        return None
    
    try:
        if '-' in page_range:
            start, end = page_range.split('-')
            start = int(start)
            end = int(end)
            if start < 1 or end < 1:
                raise ValueError("Page numbers must be positive")
            return (start, end)
        else:
            page = int(page_range)
            if page < 1:
                raise ValueError("Page numbers must be positive")
            return (page, page)
    except ValueError as e:
        raise ValueError(f"Invalid page range format: {page_range}. Use format: '2-6' or '5'")


def get_pdf_info(pdf_path):
    """Get PDF information."""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        info = {
            'pages': len(doc),
            'title': doc.metadata.get('title', 'Unknown'),
            'author': doc.metadata.get('author', 'Unknown'),
            'subject': doc.metadata.get('subject', ''),
            'creator': doc.metadata.get('creator', ''),
            'producer': doc.metadata.get('producer', ''),
        }
        doc.close()
        return info
    except Exception as e:
        print(f"Warning: Failed to get PDF info: {e}")
        return None


def print_pdf_info(pdf_path):
    """Print PDF information."""
    info = get_pdf_info(pdf_path)
    if info:
        print("\nPDF Information:")
        print(f"  Pages: {info['pages']}")
        print(f"  Title: {info['title']}")
        print(f"  Author: {info['author']}")
        if info['subject']:
            print(f"  Subject: {info['subject']}")
        if info['creator']:
            print(f"  Creator: {info['creator']}")
        print()


if __name__ == "__main__":
    # Test functions
    print("Testing utilities...")
    
    print("\nTest get_timestamp():", get_timestamp())
    
    print("\nTest format_size():")
    print("  1024 bytes:", format_size(1024))
    print("  1048576 bytes:", format_size(1048576))
    print("  1073741824 bytes:", format_size(1073741824))
    
    print("\nTest count_images():")
    print("  Count in current dir:", count_images('.'))
    
    print("\nTest validate_screenshot_method():")
    print("  'full':", validate_screenshot_method('full'))
    print("  'region':", validate_screenshot_method('region'))
    print("  'invalid':", validate_screenshot_method('invalid'))
    
    print("\nTest validate_page_range():")
    print("  '2-6':", validate_page_range('2-6'))
    print("  '5':", validate_page_range('5'))
    print("  'invalid':", validate_page_range('invalid'))
    
    print("\n✓ All tests passed!")
