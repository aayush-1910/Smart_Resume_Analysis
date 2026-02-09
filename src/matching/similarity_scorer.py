"""
Similarity Scorer Module
Calculates match scores between resumes and job descriptions.
"""
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np

from config.settings import SCORING_WEIGHTS, SKILL_IMPORTANCE_WEIGHTS, MATCH_THRESHOLDS
from config.logging_config import get_logger
from src.feature_engineering.vectorizer import calculate_cosine_similarity

logger = get_logger("similarity_scorer")


def calculate_match_score(
    resume_vector: np.ndarray,
    job_vector: np.ndarray,
    resume_skills: List[str],
    required_skills: List[Dict],
    weights: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Calculate match score between resume and job description.
    
    Args:
        resume_vector: Vector representation of resume (300-dim)
        job_vector: Vector representation of job description (300-dim)
        resume_skills: List of skill names from resume
        required_skills: List of dicts with 'skill_name' and 'importance'
        weights: Optional custom weights for scoring
        
    Returns:
        Match result dictionary following MatchResult schema
    """
    if weights is None:
        weights = SCORING_WEIGHTS.copy()
    
    # Validate vector dimensions
    if resume_vector.shape[0] != 300 or job_vector.shape[0] != 300:
        logger.error("INVALID_VECTOR_DIMENSION: Vectors must be 300-dimensional")
        raise ValueError("INVALID_VECTOR_DIMENSION: Vectors must be 300-dimensional")
    
    # Calculate semantic similarity
    semantic_similarity = calculate_cosine_similarity(resume_vector, job_vector)
    
    # Calculate skill match score
    skill_match, matched_skills, missing_skills = calculate_skill_match(
        resume_skills, required_skills
    )
    
    # Calculate overall score
    overall_score = (
        skill_match * weights.get('skill_match', 0.5) +
        semantic_similarity * weights.get('semantic_similarity', 0.5)
    )
    
    # Determine recommendation
    recommendation = get_recommendation(overall_score)
    
    # Build result
    result = {
        "match_id": str(uuid.uuid4()),
        "resume_id": None,  # To be set by caller
        "job_id": None,  # To be set by caller
        "timestamp": datetime.utcnow().isoformat(),
        "overall_score": round(overall_score, 3),
        "subscores": {
            "skill_match": round(skill_match, 3),
            "semantic_similarity": round(semantic_similarity, 3)
        },
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation
    }
    
    return result


def calculate_skill_match(
    resume_skills: List[str],
    required_skills: List[Dict]
) -> tuple:
    """
    Calculate skill match score with importance weighting.
    
    Args:
        resume_skills: List of skill names from resume
        required_skills: List of dicts with 'skill_name' and 'importance'
        
    Returns:
        Tuple of (score, matched_skills, missing_skills)
    """
    if not required_skills:
        # No required skills - use semantic similarity only
        return 1.0, [], []
    
    resume_skills_lower = [s.lower() for s in resume_skills]
    
    matched_skills = []
    missing_skills = []
    weighted_sum = 0.0
    total_weight = 0.0
    
    for req_skill in required_skills:
        skill_name = req_skill.get('skill_name', '')
        importance = req_skill.get('importance', 'preferred')
        weight = SKILL_IMPORTANCE_WEIGHTS.get(importance, 0.6)
        
        total_weight += weight
        
        # Check if resume has this skill
        if skill_name.lower() in resume_skills_lower:
            matched_skills.append(skill_name)
            weighted_sum += weight
        else:
            missing_skills.append({
                "skill_name": skill_name,
                "importance": importance
            })
    
    # Calculate score
    score = weighted_sum / total_weight if total_weight > 0 else 0.0
    
    return score, matched_skills, missing_skills


def get_recommendation(score: float) -> str:
    """
    Get recommendation label based on score.
    
    Args:
        score: Overall match score (0.0-1.0)
        
    Returns:
        Recommendation string
    """
    if score >= MATCH_THRESHOLDS['strong-match']:
        return 'strong-match'
    elif score >= MATCH_THRESHOLDS['good-match']:
        return 'good-match'
    elif score >= MATCH_THRESHOLDS['weak-match']:
        return 'weak-match'
    else:
        return 'no-match'


def batch_calculate_scores(
    resume_vectors: List[np.ndarray],
    job_vector: np.ndarray,
    resume_skills_list: List[List[str]],
    required_skills: List[Dict]
) -> List[Dict[str, Any]]:
    """
    Calculate match scores for multiple resumes against one job.
    
    Args:
        resume_vectors: List of resume vectors
        job_vector: Job description vector
        resume_skills_list: List of skill lists for each resume
        required_skills: Required skills from job
        
    Returns:
        List of match results sorted by score
    """
    results = []
    
    for i, (vector, skills) in enumerate(zip(resume_vectors, resume_skills_list)):
        result = calculate_match_score(vector, job_vector, skills, required_skills)
        result['resume_index'] = i
        results.append(result)
    
    # Sort by overall score descending
    results.sort(key=lambda x: x['overall_score'], reverse=True)
    
    return results


if __name__ == "__main__":
    # Test scoring
    resume_vec = np.random.randn(300)
    job_vec = np.random.randn(300)
    
    resume_skills = ['Python', 'JavaScript', 'React', 'Machine Learning']
    required_skills = [
        {'skill_name': 'Python', 'importance': 'critical'},
        {'skill_name': 'React', 'importance': 'preferred'},
        {'skill_name': 'AWS', 'importance': 'nice-to-have'},
        {'skill_name': 'Docker', 'importance': 'preferred'}
    ]
    
    result = calculate_match_score(resume_vec, job_vec, resume_skills, required_skills)
    print("Match Result:")
    print(f"  Overall Score: {result['overall_score']}")
    print(f"  Skill Match: {result['subscores']['skill_match']}")
    print(f"  Semantic Similarity: {result['subscores']['semantic_similarity']}")
    print(f"  Recommendation: {result['recommendation']}")
    print(f"  Matched Skills: {result['matched_skills']}")
    print(f"  Missing Skills: {result['missing_skills']}")
