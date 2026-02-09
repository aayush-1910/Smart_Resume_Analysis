"""Tests for preprocessing module."""
import pytest
import os
from pathlib import Path


def test_text_cleaner():
    """Test text cleaning function."""
    from src.preprocessing.text_cleaner import clean_text
    
    # Test whitespace cleaning
    text = "Hello    World\n\n\n\nTest"
    cleaned = clean_text(text)
    assert "  " not in cleaned
    
    # Test empty input
    assert clean_text("") == ""
    assert clean_text(None) == ""


def test_parser_email():
    """Test email extraction."""
    from src.preprocessing.parser import extract_email
    
    assert extract_email("Contact: test@example.com") == "test@example.com"
    assert extract_email("No email here") is None


def test_parser_phone():
    """Test phone extraction."""
    from src.preprocessing.parser import extract_phone
    
    text = "Call me at (555) 123-4567"
    phone = extract_phone(text)
    assert phone is not None
    assert "555" in phone


def test_parser_name():
    """Test name extraction."""
    from src.preprocessing.parser import extract_name
    
    text = "John Doe\njohn@example.com\n555-1234"
    name = extract_name(text)
    assert name == "John Doe"
