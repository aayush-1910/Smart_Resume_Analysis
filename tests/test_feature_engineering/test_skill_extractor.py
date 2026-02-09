"""Tests for feature engineering module."""
import pytest


def test_skill_extractor():
    """Test skill extraction."""
    from src.feature_engineering.skill_extractor import extract_skills
    
    text = "Experienced Python developer with React and Machine Learning expertise."
    skills = extract_skills(text)
    
    skill_names = [s['skill_name'] for s in skills]
    assert 'Python' in skill_names
    assert 'React' in skill_names
    assert 'Machine Learning' in skill_names


def test_skill_confidence():
    """Test skill confidence calculation."""
    from src.feature_engineering.skill_extractor import calculate_skill_confidence
    
    # Single mention
    conf1 = calculate_skill_confidence("Python", "I know Python")
    assert 0.6 <= conf1 <= 1.0
    
    # Multiple mentions should have higher confidence
    conf2 = calculate_skill_confidence("Python", "Python Python Python expert in Python")
    assert conf2 >= conf1


def test_keyword_extraction():
    """Test keyword extraction."""
    from src.feature_engineering.keyword_analyzer import extract_keywords
    
    text = "Python development with machine learning and data science."
    keywords = extract_keywords(text)
    
    assert len(keywords) > 0
    keyword_texts = [k['keyword'] for k in keywords]
    assert 'python' in keyword_texts or 'development' in keyword_texts
