"""
Text Cleaner Module
Cleans and normalizes extracted text from resumes.
"""
import re
import unicodedata
from typing import Optional

from config.logging_config import get_logger

logger = get_logger("text_cleaner")


def clean_text(
    text: str,
    remove_extra_whitespace: bool = True,
    normalize_unicode: bool = True,
    remove_special_chars: bool = False,
    lowercase: bool = False
) -> str:
    """
    Clean and normalize text extracted from resumes.
    
    Args:
        text: Raw text to clean
        remove_extra_whitespace: Collapse multiple whitespace to single space
        normalize_unicode: Convert unicode characters to ASCII equivalents
        remove_special_chars: Remove non-alphanumeric characters
        lowercase: Convert text to lowercase
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    cleaned = text
    
    # Normalize unicode characters
    if normalize_unicode:
        cleaned = unicodedata.normalize('NFKD', cleaned)
        cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')
    
    # Remove special characters (keeping letters, numbers, basic punctuation)
    if remove_special_chars:
        cleaned = re.sub(r'[^a-zA-Z0-9\s.,;:!?\-@#$%&*()\[\]{}\'\"]+', '', cleaned)
    
    # Remove extra whitespace
    if remove_extra_whitespace:
        # Replace multiple spaces/tabs with single space
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        # Replace multiple newlines with double newline
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        # Strip leading/trailing whitespace from lines
        lines = [line.strip() for line in cleaned.split('\n')]
        cleaned = '\n'.join(lines)
    
    # Convert to lowercase
    if lowercase:
        cleaned = cleaned.lower()
    
    # Final strip
    cleaned = cleaned.strip()
    
    return cleaned


def remove_headers_footers(text: str) -> str:
    """
    Remove common header/footer patterns from resume text.
    
    Args:
        text: Text to process
        
    Returns:
        Text with headers/footers removed
    """
    lines = text.split('\n')
    cleaned_lines = []
    
    # Patterns to skip (page numbers, dates, etc.)
    skip_patterns = [
        r'^Page\s+\d+\s*(of\s+\d+)?$',  # Page X of Y
        r'^\d+\s*$',  # Just page numbers
        r'^Confidential\s*$',  # Confidentiality notices
        r'^Resume\s+of\s+',  # "Resume of X" headers
    ]
    
    for line in lines:
        stripped = line.strip()
        should_skip = any(re.match(pattern, stripped, re.IGNORECASE) 
                        for pattern in skip_patterns)
        if not should_skip:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def extract_sections(text: str) -> dict:
    """
    Attempt to extract common resume sections.
    
    Args:
        text: Resume text
        
    Returns:
        Dictionary with section names as keys and content as values
    """
    sections = {}
    
    # Common section headers
    section_patterns = [
        (r'(?i)\b(education|academic)\b', 'education'),
        (r'(?i)\b(experience|work\s*history|employment)\b', 'experience'),
        (r'(?i)\b(skills|technical\s*skills|competencies)\b', 'skills'),
        (r'(?i)\b(summary|profile|objective)\b', 'summary'),
        (r'(?i)\b(projects|portfolio)\b', 'projects'),
        (r'(?i)\b(certifications?|licenses?)\b', 'certifications'),
        (r'(?i)\b(awards?|achievements?|honors?)\b', 'awards'),
    ]
    
    lines = text.split('\n')
    current_section = 'header'
    current_content = []
    
    for line in lines:
        # Check if line is a section header
        found_section = None
        for pattern, section_name in section_patterns:
            if re.search(pattern, line) and len(line.strip()) < 50:
                found_section = section_name
                break
        
        if found_section:
            # Save previous section
            if current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = found_section
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections


if __name__ == "__main__":
    # Test text cleaning
    sample = """
    John   Doe
    Software    Engineer
    
    
    
    Email: john.doe@email.com
    
    EXPERIENCE
    
    Senior Developer at Tech Corp
    """
    
    cleaned = clean_text(sample)
    print("Cleaned text:")
    print(cleaned)
    print("\nSections:")
    print(extract_sections(cleaned))
