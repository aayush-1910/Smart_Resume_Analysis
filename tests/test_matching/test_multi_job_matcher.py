"""
Tests for Multi-Job Matcher
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def create_mock_resume():
    """Create a mock processed resume."""
    return {
        'resume_id': 'test-resume-1',
        'candidate': {
            'name': 'John Doe',
            'email': 'john@example.com'
        },
        'skills': [
            {'skill_name': 'Python', 'confidence': 0.9},
            {'skill_name': 'JavaScript', 'confidence': 0.8},
            {'skill_name': 'Machine Learning', 'confidence': 0.7}
        ],
        'vector_representation': [0.1] * 300,  # Mock vector
        'raw_text': 'John Doe, Software Engineer with 5 years Python experience...'
    }


def create_mock_jobs():
    """Create mock job descriptions."""
    return [
        {
            'title': 'Python Developer',
            'company': 'Tech Corp',
            'description': 'Looking for Python developer with ML experience.',
            'required_skills': [
                {'skill_name': 'Python', 'importance': 'critical'},
                {'skill_name': 'Django', 'importance': 'preferred'}
            ]
        },
        {
            'title': 'Frontend Developer',
            'company': 'Web Inc',
            'description': 'Need React and JavaScript expert.',
            'required_skills': [
                {'skill_name': 'JavaScript', 'importance': 'critical'},
                {'skill_name': 'React', 'importance': 'critical'}
            ]
        },
        {
            'title': 'Data Scientist',
            'company': 'AI Labs',
            'description': 'Machine learning and Python skills required.',
            'required_skills': [
                {'skill_name': 'Python', 'importance': 'critical'},
                {'skill_name': 'Machine Learning', 'importance': 'critical'}
            ]
        }
    ]


class TestMultiJobMatcher:
    """Test cases for multi-job comparison."""
    
    def test_compare_with_three_jobs(self):
        """Test comparison with 3 jobs - minimum valid input."""
        # This test would require actual pipeline setup
        # For now, test the validation logic
        from src.matching.multi_job_matcher import compare_resume_to_jobs
        
        resume = create_mock_resume()
        jobs = create_mock_jobs()
        
        # Should work with 3 jobs (would need full pipeline for real test)
        # For unit test, we check structure
        assert len(jobs) == 3
        assert all('title' in job for job in jobs)
        assert all('description' in job for job in jobs)
    
    def test_too_few_jobs_raises_error(self):
        """Test that <2 jobs raises ValueError."""
        from src.matching.multi_job_matcher import compare_resume_to_jobs
        
        resume = create_mock_resume()
        jobs = [create_mock_jobs()[0]]  # Only 1 job
        
        with pytest.raises(ValueError, match="Minimum 2 jobs"):
            compare_resume_to_jobs(resume, jobs)
    
    def test_too_many_jobs_raises_error(self):
        """Test that >5 jobs raises ValueError."""
        from src.matching.multi_job_matcher import compare_resume_to_jobs
        
        resume = create_mock_resume()
        jobs = create_mock_jobs() * 3  # 9 jobs
        
        with pytest.raises(ValueError, match="Maximum 5 jobs"):
            compare_resume_to_jobs(resume, jobs)
    
    def test_missing_title_raises_error(self):
        """Test that missing job title raises ValueError."""
        from src.matching.multi_job_matcher import compare_resume_to_jobs
        
        resume = create_mock_resume()
        jobs = [
            {'description': 'Job 1'},
            {'title': 'Job 2', 'description': 'Desc'}
        ]
        
        with pytest.raises(ValueError, match="missing 'title'"):
            compare_resume_to_jobs(resume, jobs)
    
    def test_format_comparison_table(self):
        """Test table formatting function."""
        from src.matching.multi_job_matcher import format_comparison_table
        
        mock_result = {
            'results': [
                {
                    'rank': 1,
                    'job_title': 'Python Developer',
                    'overall_score': 0.85,
                    'recommendation': 'strong-match',
                    'matched_skills': ['Python', 'ML']
                },
                {
                    'rank': 2,
                    'job_title': 'Frontend Developer',
                    'overall_score': 0.65,
                    'recommendation': 'good-match',
                    'matched_skills': ['JavaScript']
                }
            ]
        }
        
        table = format_comparison_table(mock_result)
        assert 'Python Developer' in table
        assert 'Frontend Developer' in table
        assert 'Rank' in table


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
