"""
Validators Module
Input validation utilities.
"""
from pathlib import Path
from typing import Tuple

from config.settings import MAX_FILE_SIZE_BYTES, MAX_RESUME_PAGES, MIN_TEXT_LENGTH


def validate_pdf(file_path: str) -> Tuple[bool, str]:
    """
    Validate PDF file.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    path = Path(file_path)
    
    if not path.exists():
        return False, "PDF_FILE_NOT_FOUND: File does not exist"
    
    if not path.suffix.lower() == '.pdf':
        return False, "INVALID_FILE_TYPE: File must be a PDF"
    
    file_size = path.stat().st_size
    if file_size > MAX_FILE_SIZE_BYTES:
        return False, f"PDF_TOO_LARGE: File exceeds {MAX_FILE_SIZE_BYTES / (1024*1024):.1f}MB limit"
    
    if file_size == 0:
        return False, "PDF_CORRUPTED: File is empty"
    
    return True, ""


def validate_text_length(text: str, min_length: int = MIN_TEXT_LENGTH) -> Tuple[bool, str]:
    """
    Validate text length.
    
    Args:
        text: Text to validate
        min_length: Minimum required length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or len(text.strip()) < min_length:
        return False, f"TEXT_TOO_SHORT: Text must be at least {min_length} characters"
    
    return True, ""


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_skills_list(skills: list) -> Tuple[bool, str]:
    """
    Validate skills list format.
    
    Args:
        skills: List of skill dictionaries
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(skills, list):
        return False, "Skills must be a list"
    
    for skill in skills:
        if not isinstance(skill, dict):
            return False, "Each skill must be a dictionary"
        if 'skill_name' not in skill:
            return False, "Each skill must have 'skill_name' field"
    
    return True, ""
