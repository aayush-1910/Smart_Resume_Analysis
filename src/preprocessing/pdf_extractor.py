"""
PDF Text Extractor Module
Extracts text content from PDF resume files.
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path

# PDF processing libraries (imported conditionally)
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import (
    MAX_FILE_SIZE_BYTES,
    MAX_RESUME_PAGES,
    MAX_EXTRACTED_TEXT_LENGTH,
    PROCESSING_TIMEOUT_SECONDS
)
from config.logging_config import get_logger

logger = get_logger("pdf_extractor")


class PDFExtractionError(Exception):
    """Custom exception for PDF extraction errors."""
    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(f"{error_code}: {message}")


def extract_text_from_pdf(
    file_path: str,
    method: str = 'pdfplumber'
) -> Dict[str, Any]:
    """
    Extract text content from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        method: Extraction method ('pdfplumber' or 'pypdf2')
        
    Returns:
        Dictionary containing:
            - text: Extracted text content
            - num_pages: Number of pages in PDF
            - file_size_bytes: Size of the file
            - extraction_method: Method used for extraction
            - success: Boolean indicating success
            - error: Error message if failed
            
    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file exceeds size or page limits
    """
    result = {
        "text": "",
        "num_pages": 0,
        "file_size_bytes": 0,
        "extraction_method": method,
        "success": False,
        "error": None
    }
    
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        raise PDFExtractionError("PDF_FILE_NOT_FOUND", f"File does not exist: {file_path}")
    
    # Check file size
    file_size = path.stat().st_size
    result["file_size_bytes"] = file_size
    
    if file_size > MAX_FILE_SIZE_BYTES:
        raise PDFExtractionError(
            "PDF_TOO_LARGE",
            f"File exceeds {MAX_FILE_SIZE_BYTES / (1024*1024):.1f}MB limit"
        )
    
    try:
        if method == 'pdfplumber' and PDFPLUMBER_AVAILABLE:
            text, num_pages = _extract_with_pdfplumber(file_path)
        elif PYPDF2_AVAILABLE:
            text, num_pages = _extract_with_pypdf2(file_path)
            result["extraction_method"] = "pypdf2"
        else:
            raise PDFExtractionError(
                "PDF_LIBRARY_NOT_FOUND",
                "No PDF extraction library available"
            )
        
        # Check page limit
        if num_pages > MAX_RESUME_PAGES:
            raise PDFExtractionError(
                "PDF_TOO_MANY_PAGES",
                f"PDF has {num_pages} pages, exceeds limit of {MAX_RESUME_PAGES}"
            )
        
        # Check if text was extracted
        if not text or not text.strip():
            raise PDFExtractionError(
                "PDF_NO_TEXT",
                "No extractable text found (may be scanned image)"
            )
        
        # Truncate if necessary
        if len(text) > MAX_EXTRACTED_TEXT_LENGTH:
            logger.warning(f"Text truncated from {len(text)} to {MAX_EXTRACTED_TEXT_LENGTH} chars")
            text = text[:MAX_EXTRACTED_TEXT_LENGTH]
        
        result["text"] = text
        result["num_pages"] = num_pages
        result["success"] = True
        
    except PDFExtractionError:
        raise
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        raise PDFExtractionError("PDF_CORRUPTED", f"Failed to process PDF: {str(e)}")
    
    return result


def _extract_with_pdfplumber(file_path: str) -> tuple:
    """Extract text using pdfplumber (better for multi-column layouts)."""
    text_parts = []
    num_pages = 0
    
    with pdfplumber.open(file_path) as pdf:
        num_pages = len(pdf.pages)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    
    return "\n\n".join(text_parts), num_pages


def _extract_with_pypdf2(file_path: str) -> tuple:
    """Extract text using PyPDF2 (fallback method)."""
    text_parts = []
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    
    return "\n\n".join(text_parts), num_pages


if __name__ == "__main__":
    # Test with a sample PDF
    import sys
    if len(sys.argv) > 1:
        result = extract_text_from_pdf(sys.argv[1])
        print(f"Pages: {result['num_pages']}")
        print(f"Size: {result['file_size_bytes']} bytes")
        print(f"Text preview: {result['text'][:500]}...")
