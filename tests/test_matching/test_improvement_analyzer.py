"""
Tests for Improvement Analyzer
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def create_mock_resume_good():
    """Create a mock resume with good content."""
    return {
        'resume_id': 'test-resume-1',
        'candidate': {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890'
        },
        'skills': [
            {'skill_name': 'Python', 'confidence': 0.9},
            {'skill_name': 'JavaScript', 'confidence': 0.8},
            {'skill_name': 'Communication', 'confidence': 0.7}
        ],
        'raw_text': '''John Doe
        john@example.com | +1234567890
        
        Education
        Bachelor of Science in Computer Science, MIT, 2020
        
        Experience
        Senior Software Engineer at Tech Corp (2020-Present)
        - Developed Python applications serving 1M+ users
        - Led team of 5 engineers
        - Improved performance by 30%
        
        Skills
        Python, JavaScript, React, Machine Learning, AWS, Docker
        '''
    }


def create_mock_resume_bad():
    """Create a mock resume with issues."""
    return {
        'resume_id': 'test-resume-2',
        'candidate': {
            'name': '',
            'email': None,
            'phone': None
        },
        'skills': [],
        'raw_text': 'Short resume text'
    }


def create_mock_job():
    """Create a mock job description."""
    return {
        'job_id': 'test-job-1',
        'title': 'Senior Python Developer',
        'description': 'Looking for Python developer with ML experience and AWS skills.',
        'required_skills': [
            {'skill_name': 'Python', 'importance': 'critical'},
            {'skill_name': 'Machine Learning', 'importance': 'critical'},
            {'skill_name': 'AWS', 'importance': 'preferred'}
        ]
    }


def create_mock_match_result():
    """Create a mock match result."""
    return {
        'overall_score': 0.65,
        'recommendation': 'good-match',
        'matched_skills': ['Python', 'JavaScript'],
        'missing_skills': [
            {'skill_name': 'Machine Learning', 'importance': 'critical'},
            {'skill_name': 'AWS', 'importance': 'preferred'}
        ]
    }


class TestImprovementAnalyzer:
    """Test cases for improvement analyzer."""
    
    def test_good_resume_has_fewer_suggestions(self):
        """Test that a good resume generates fewer high-priority suggestions."""
        from src.matching.improvement_analyzer import generate_improvement_suggestions
        
        resume = create_mock_resume_good()
        job = create_mock_job()
        match_result = create_mock_match_result()
        
        result = generate_improvement_suggestions(resume, job, match_result)
        
        high_priority = [s for s in result['suggestions'] if s['priority'] == 'high']
        # Good resume should have few high priority issues
        assert len(high_priority) <= 2
    
    def test_bad_resume_flags_contact_info(self):
        """Test that missing contact info is flagged as high priority."""
        from src.matching.improvement_analyzer import generate_improvement_suggestions
        
        resume = create_mock_resume_bad()
        job = create_mock_job()
        match_result = create_mock_match_result()
        
        result = generate_improvement_suggestions(resume, job, match_result)
        
        # Should have contact info suggestion
        categories = [s['category'] for s in result['suggestions']]
        assert 'formatting' in categories
    
    def test_short_resume_flagged(self):
        """Test that short resume is flagged."""
        from src.matching.improvement_analyzer import generate_improvement_suggestions
        
        resume = create_mock_resume_bad()
        job = create_mock_job()
        match_result = create_mock_match_result()
        
        result = generate_improvement_suggestions(resume, job, match_result)
        
        # Should have formatting suggestion about length
        titles = [s['title'] for s in result['suggestions']]
        assert any('Short' in t or 'Contact' in t for t in titles)
    
    def test_quality_score_in_range(self):
        """Test quality score is in 0-100 range."""
        from src.matching.improvement_analyzer import generate_improvement_suggestions
        
        resume = create_mock_resume_good()
        job = create_mock_job()
        match_result = create_mock_match_result()
        
        result = generate_improvement_suggestions(resume, job, match_result)
        
        score = result['overall_resume_quality_score']
        assert 0 <= score <= 100
    
    def test_positive_points_generated(self):
        """Test that positive points are generated for good resumes."""
        from src.matching.improvement_analyzer import generate_improvement_suggestions
        
        resume = create_mock_resume_good()
        job = create_mock_job()
        match_result = create_mock_match_result()
        
        result = generate_improvement_suggestions(resume, job, match_result)
        
        assert 'positive_points' in result
        assert len(result['positive_points']) > 0
    
    def test_suggestions_have_action_items(self):
        """Test that suggestions include actionable items."""
        from src.matching.improvement_analyzer import generate_improvement_suggestions
        
        resume = create_mock_resume_bad()
        job = create_mock_job()
        match_result = create_mock_match_result()
        
        result = generate_improvement_suggestions(resume, job, match_result)
        
        for suggestion in result['suggestions']:
            assert 'action_items' in suggestion
            assert len(suggestion['action_items']) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
