"""Tests for synonym-based skill matching.

Validates that skill_synonyms.json is properly loaded and used
to normalize abbreviations/variants during skill extraction and matching.
"""
import pytest
import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestSynonymLoading:
    """Test synonym file loading."""

    def test_load_skill_synonyms(self):
        """Verify synonyms load successfully."""
        from src.feature_engineering.skill_extractor import load_skill_synonyms
        
        synonyms = load_skill_synonyms()
        assert isinstance(synonyms, dict)
        assert len(synonyms) > 0, "Synonyms file should have entries"

    def test_synonym_has_common_mappings(self):
        """Check expected mappings exist."""
        from src.feature_engineering.skill_extractor import load_skill_synonyms
        
        synonyms = load_skill_synonyms()
        # These are in skill_synonyms.json
        assert synonyms.get("JS") == "JavaScript"
        assert synonyms.get("K8s") == "Kubernetes"
        assert synonyms.get("ReactJS") == "React"


class TestSynonymNormalization:
    """Test text normalization via synonyms."""

    def test_normalize_expands_abbreviations(self):
        """JS in text should result in JavaScript being appended."""
        from src.feature_engineering.skill_extractor import normalize_text_with_synonyms
        
        text = "Experienced developer with JS and K8s skills."
        normalized = normalize_text_with_synonyms(text)
        
        assert "JavaScript" in normalized
        assert "Kubernetes" in normalized

    def test_normalize_preserves_original(self):
        """Original text should remain untouched."""
        from src.feature_engineering.skill_extractor import normalize_text_with_synonyms
        
        text = "Python developer with React experience."
        normalized = normalize_text_with_synonyms(text)
        
        assert "Python developer with React experience." in normalized

    def test_normalize_handles_empty(self):
        """Empty text should return empty."""
        from src.feature_engineering.skill_extractor import normalize_text_with_synonyms
        
        assert normalize_text_with_synonyms("") == ""


class TestSynonymSkillExtraction:
    """Test that synonym normalization improves skill extraction."""

    def test_extract_skills_with_abbreviation(self):
        """Abbreviation 'JS' should result in 'JavaScript' being extracted."""
        from src.feature_engineering.skill_extractor import extract_skills
        
        text = (
            "Full-stack developer with 5 years of experience in JS and Node. "
            "Built RESTful APIs with Express and deployed on K8s clusters. "
            "Proficient in ReactJS for frontend development and PostgreSQL databases. "
            "Experience with CI/CD pipelines using Docker containers."
        )
        skills = extract_skills(text)
        skill_names = [s['skill_name'] for s in skills]
        
        assert 'JavaScript' in skill_names, f"Expected 'JavaScript' from 'JS', got: {skill_names}"
        assert 'Kubernetes' in skill_names, f"Expected 'Kubernetes' from 'K8s', got: {skill_names}"
        assert 'React' in skill_names, f"Expected 'React' from 'ReactJS', got: {skill_names}"


class TestSynonymSkillMatching:
    """Test that synonym normalization improves skill matching in scorer."""

    def test_synonym_match_in_scorer(self):
        """'ReactJS' in resume should match 'React' in job requirements."""
        from src.matching.similarity_scorer import calculate_skill_match
        
        resume_skills = ['ReactJS', 'Python', 'Node.js']
        required_skills = [
            {'skill_name': 'React', 'importance': 'critical'},
            {'skill_name': 'Python', 'importance': 'preferred'},
        ]
        
        score, matched, missing = calculate_skill_match(resume_skills, required_skills)
        
        assert 'React' in matched, f"Expected 'React' to match via synonym, matched={matched}, missing={missing}"
        assert 'Python' in matched
        assert score > 0.8, f"Score should be high with good matches, got {score}"

    def test_direct_match_still_works(self):
        """Direct skill name matches should still work."""
        from src.matching.similarity_scorer import calculate_skill_match
        
        resume_skills = ['Python', 'Docker', 'AWS']
        required_skills = [
            {'skill_name': 'Python', 'importance': 'critical'},
            {'skill_name': 'Docker', 'importance': 'preferred'},
            {'skill_name': 'Kubernetes', 'importance': 'nice-to-have'},
        ]
        
        score, matched, missing = calculate_skill_match(resume_skills, required_skills)
        
        assert 'Python' in matched
        assert 'Docker' in matched
        assert len(missing) == 1
        assert missing[0]['skill_name'] == 'Kubernetes'
