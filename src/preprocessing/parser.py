"""
Resume Parser Module
Parses structured information from resume text (name, email, phone, etc.).
"""
import re
from typing import Dict, Any, Optional, List

from config.logging_config import get_logger

logger = get_logger("parser")


def parse_resume_info(text: str) -> Dict[str, Any]:
    """
    Parse structured information from resume text.
    
    Args:
        text: Cleaned resume text
        
    Returns:
        Dictionary containing:
            - name: Candidate name (or 'Unknown')
            - email: Email address (or None)
            - phone: Phone number (or None)
            - linkedin: LinkedIn URL (or None)
            - github: GitHub URL (or None)
    """
    result = {
        "name": "Unknown",
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None
    }
    
    # Extract email
    email = extract_email(text)
    if email:
        result["email"] = email
    
    # Extract phone
    phone = extract_phone(text)
    if phone:
        result["phone"] = phone
    
    # Extract LinkedIn
    linkedin = extract_linkedin(text)
    if linkedin:
        result["linkedin"] = linkedin
    
    # Extract GitHub
    github = extract_github(text)
    if github:
        result["github"] = github
    
    # Extract name (usually first non-empty line or before email)
    name = extract_name(text)
    if name:
        result["name"] = name
    
    return result


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    # Various phone formats
    phone_patterns = [
        r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # US format
        r'\+?[0-9]{1,3}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}',  # International
        r'\b[0-9]{10,12}\b',  # Plain numbers
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            phone = match.group(0)
            # Clean up the phone number
            cleaned = re.sub(r'[^\d+]', '', phone)
            if len(cleaned) >= 10:
                return phone
    
    return None


def extract_linkedin(text: str) -> Optional[str]:
    """Extract LinkedIn URL from text."""
    linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
    match = re.search(linkedin_pattern, text, re.IGNORECASE)
    return match.group(0) if match else None


def extract_github(text: str) -> Optional[str]:
    """Extract GitHub URL from text."""
    github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+'
    match = re.search(github_pattern, text, re.IGNORECASE)
    return match.group(0) if match else None


def extract_name(text: str) -> Optional[str]:
    """
    Extract candidate name from resume text.
    Usually the first meaningful line or line before contact info.
    """
    lines = text.strip().split('\n')
    
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Skip lines that look like contact info
        if '@' in line or re.search(r'\d{3}[-.\s]?\d{3}', line):
            continue
        
        # Skip common headers
        skip_words = ['resume', 'curriculum', 'vitae', 'cv', 'page']
        if any(word in line.lower() for word in skip_words):
            continue
        
        # Check if line looks like a name (2-4 words, starts with capital)
        words = line.split()
        if 1 <= len(words) <= 4:
            if all(word[0].isupper() for word in words if word):
                return line
    
    return None


def extract_years_of_experience(text: str) -> Optional[int]:
    """
    Attempt to extract years of experience from resume text.
    
    Args:
        text: Resume text
        
    Returns:
        Estimated years of experience or None
    """
    # Look for explicit mentions
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'experience[:\s]*(\d+)\+?\s*years?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                pass
    
    return None


def extract_education_level(text: str) -> Optional[str]:
    """
    Extract highest education level mentioned in resume.
    
    Args:
        text: Resume text
        
    Returns:
        Education level string or None
    """
    education_levels = [
        (r'\b(?:ph\.?d|doctorate|doctoral)\b', 'PhD'),
        (r'\b(?:master\'?s?|m\.?s\.?|m\.?a\.?|mba|m\.?tech)\b', 'Masters'),
        (r'\b(?:bachelor\'?s?|b\.?s\.?|b\.?a\.?|b\.?tech|b\.?e\.?)\b', 'Bachelors'),
        (r'\b(?:associate\'?s?|a\.?s\.?|a\.?a\.?)\b', 'Associates'),
        (r'\b(?:high\s*school|diploma)\b', 'High School'),
    ]
    
    text_lower = text.lower()
    
    for pattern, level in education_levels:
        if re.search(pattern, text_lower):
            return level
    
    return None


if __name__ == "__main__":
    # Test parsing
    sample = """
    John Doe
    john.doe@email.com
    (555) 123-4567
    linkedin.com/in/johndoe
    github.com/johndoe
    
    Software Engineer with 5+ years of experience
    
    Education
    Master of Science in Computer Science
    """
    
    result = parse_resume_info(sample)
    print("Parsed info:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    print(f"\nYears of experience: {extract_years_of_experience(sample)}")
    print(f"Education level: {extract_education_level(sample)}")
