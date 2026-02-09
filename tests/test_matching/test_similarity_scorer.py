"""Tests for matching module."""
import pytest
import numpy as np


def test_similarity_scorer():
    """Test match score calculation."""
    from src.matching.similarity_scorer import calculate_match_score
    
    # Create test vectors
    resume_vec = np.random.randn(300)
    job_vec = np.random.randn(300)
    
    resume_skills = ['Python', 'React', 'Machine Learning']
    required_skills = [
        {'skill_name': 'Python', 'importance': 'critical'},
        {'skill_name': 'AWS', 'importance': 'preferred'}
    ]
    
    result = calculate_match_score(resume_vec, job_vec, resume_skills, required_skills)
    
    assert 'overall_score' in result
    assert 0 <= result['overall_score'] <= 1
    assert 'matched_skills' in result
    assert 'missing_skills' in result
    assert 'Python' in result['matched_skills']


def test_recommendation_thresholds():
    """Test recommendation mapping."""
    from src.matching.similarity_scorer import get_recommendation
    
    assert get_recommendation(0.80) == 'strong-match'
    assert get_recommendation(0.60) == 'good-match'
    assert get_recommendation(0.40) == 'weak-match'
    assert get_recommendation(0.20) == 'no-match'


def test_explainer():
    """Test explanation generation."""
    from src.matching.explainer import generate_match_explanation
    
    result = {
        'overall_score': 0.72,
        'recommendation': 'good-match',
        'subscores': {'skill_match': 0.65, 'semantic_similarity': 0.79},
        'matched_skills': ['Python'],
        'missing_skills': [{'skill_name': 'AWS', 'importance': 'critical'}]
    }
    
    explanation = generate_match_explanation(result)
    assert 'good-match' in explanation.lower() or 'good match' in explanation.lower()
    assert 'Python' in explanation
