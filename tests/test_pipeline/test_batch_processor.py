"""
Tests for Batch Processor
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestBatchProcessor:
    """Test cases for batch processing."""
    
    def test_too_few_resumes_raises_error(self):
        """Test that <2 resumes raises ValueError."""
        from src.pipeline.batch_processor import batch_process_resumes
        
        job = {'title': 'Developer', 'description': 'Python dev needed'}
        
        with pytest.raises(ValueError, match="Minimum 2 resumes"):
            batch_process_resumes(['single_file.pdf'], job)
    
    def test_too_many_resumes_raises_error(self):
        """Test that >10 resumes raises ValueError."""
        from src.pipeline.batch_processor import batch_process_resumes
        
        job = {'title': 'Developer', 'description': 'Python dev needed'}
        files = [f'resume_{i}.pdf' for i in range(15)]
        
        with pytest.raises(ValueError, match="Maximum 10 resumes"):
            batch_process_resumes(files, job)
    
    def test_export_csv_format(self):
        """Test CSV export format."""
        from src.pipeline.batch_processor import export_batch_results_csv
        
        mock_result = {
            'results': [
                {
                    'rank': 1,
                    'candidate_name': 'John Doe',
                    'candidate_email': 'john@example.com',
                    'filename': 'john_resume.pdf',
                    'overall_score': 0.85,
                    'subscores': {'skill_match': 0.8, 'semantic_similarity': 0.9},
                    'recommendation': 'strong-match',
                    'matched_skills': ['Python'],
                    'missing_skills': []
                }
            ]
        }
        
        csv = export_batch_results_csv(mock_result)
        assert 'Rank,Candidate Name' in csv
        assert 'John Doe' in csv
        assert '85%' in csv or '0.85' in csv
    
    def test_get_batch_statistics(self):
        """Test statistics calculation."""
        from src.pipeline.batch_processor import get_batch_statistics
        
        mock_result = {
            'results': [
                {'overall_score': 0.85, 'recommendation': 'strong-match'},
                {'overall_score': 0.65, 'recommendation': 'good-match'},
                {'overall_score': 0.45, 'recommendation': 'weak-match'}
            ],
            'failed_resumes': []
        }
        
        stats = get_batch_statistics(mock_result)
        
        assert stats['total_processed'] == 3
        assert 0.6 < stats['average_score'] < 0.7
        assert stats['strong_matches'] == 1
        assert stats['good_matches'] == 1
        assert stats['weak_matches'] == 1
    
    def test_get_top_candidates(self):
        """Test top candidates extraction."""
        from src.pipeline.batch_processor import get_top_candidates
        
        mock_result = {
            'results': [
                {'rank': 1, 'candidate_name': 'Alice'},
                {'rank': 2, 'candidate_name': 'Bob'},
                {'rank': 3, 'candidate_name': 'Charlie'},
                {'rank': 4, 'candidate_name': 'Diana'}
            ]
        }
        
        top = get_top_candidates(mock_result, top_n=2)
        
        assert len(top) == 2
        assert top[0]['candidate_name'] == 'Alice'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
