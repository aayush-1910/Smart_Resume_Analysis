"""
Tests for Learning Recommender
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestLearningRecommender:
    """Test cases for learning recommendations."""
    
    def test_find_courses_for_known_skill(self):
        """Test finding courses for a skill in the database."""
        from src.recommendations.learning_recommender import find_courses_for_skill
        
        courses = find_courses_for_skill('Python')
        
        assert len(courses) > 0
        assert all('title' in c for c in courses)
        assert all('url' in c for c in courses)
    
    def test_find_courses_with_synonym(self):
        """Test skill synonym matching (ML -> Machine Learning)."""
        from src.recommendations.learning_recommender import normalize_skill_name
        
        normalized = normalize_skill_name('ML')
        assert normalized == 'Machine Learning'
    
    def test_fallback_for_unknown_skill(self):
        """Test fallback for unmapped skills."""
        from src.recommendations.learning_recommender import find_courses_for_skill
        
        courses = find_courses_for_skill('Some Unknown Skill XYZ123')
        
        assert len(courses) == 1
        assert courses[0].get('is_fallback') == True
        assert 'youtube' in courses[0].get('url', '').lower()
    
    def test_generate_recommendations_structure(self):
        """Test learning recommendations output structure."""
        from src.recommendations.learning_recommender import generate_learning_recommendations
        
        missing = [
            {'skill_name': 'Python', 'importance': 'critical'},
            {'skill_name': 'JavaScript', 'importance': 'preferred'}
        ]
        
        result = generate_learning_recommendations(missing, max_skills=2)
        
        assert 'learning_plan_id' in result
        assert 'skills' in result
        assert len(result['skills']) <= 2
        assert 'estimated_total_time' in result
    
    def test_skills_sorted_by_importance(self):
        """Test that skills are sorted by importance."""
        from src.recommendations.learning_recommender import generate_learning_recommendations
        
        missing = [
            {'skill_name': 'React', 'importance': 'nice-to-have'},
            {'skill_name': 'Python', 'importance': 'critical'},
            {'skill_name': 'AWS', 'importance': 'preferred'}
        ]
        
        result = generate_learning_recommendations(missing, max_skills=3)
        
        # First skill should be critical
        assert result['skills'][0]['importance'] == 'critical'
    
    def test_get_skill_coverage_stats(self):
        """Test skill coverage statistics."""
        from src.recommendations.learning_recommender import get_skill_coverage_stats
        
        stats = get_skill_coverage_stats()
        
        assert stats['total_skills'] >= 50  # At least 50 skills
        assert stats['total_courses'] >= 100  # At least 100 courses
        assert stats['free_courses'] > 0
    
    def test_learning_milestones_generated(self):
        """Test that learning path milestones are generated."""
        from src.recommendations.learning_recommender import generate_learning_recommendations
        
        missing = [
            {'skill_name': 'Python', 'importance': 'critical'},
            {'skill_name': 'React', 'importance': 'preferred'}
        ]
        
        result = generate_learning_recommendations(missing, max_skills=2)
        
        assert 'learning_path_milestones' in result
        assert len(result['learning_path_milestones']) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
