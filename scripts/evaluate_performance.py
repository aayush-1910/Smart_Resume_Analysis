"""
Performance Evaluation Script
Evaluate model performance on test data.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def evaluate_skill_extraction():
    """Evaluate skill extraction accuracy."""
    from src.feature_engineering import extract_skills
    
    # Test cases with expected skills
    test_cases = [
        {
            'text': 'Python developer with React and AWS experience',
            'expected': ['Python', 'React', 'AWS']
        },
        {
            'text': 'Machine learning engineer using TensorFlow and PyTorch',
            'expected': ['Machine Learning', 'TensorFlow', 'PyTorch']
        }
    ]
    
    total = 0
    correct = 0
    
    for case in test_cases:
        skills = extract_skills(case['text'])
        skill_names = [s['skill_name'] for s in skills]
        
        for expected in case['expected']:
            total += 1
            if expected in skill_names:
                correct += 1
    
    accuracy = correct / total if total > 0 else 0
    print(f"Skill Extraction Accuracy: {accuracy:.0%} ({correct}/{total})")
    return accuracy


def evaluate_scoring_consistency():
    """Evaluate scoring consistency."""
    import numpy as np
    from src.matching import calculate_match_score
    
    # Run same inputs multiple times
    resume_vec = np.random.randn(300)
    job_vec = np.random.randn(300)
    skills = ['Python', 'AWS']
    required = [{'skill_name': 'Python', 'importance': 'critical'}]
    
    scores = []
    for _ in range(10):
        result = calculate_match_score(resume_vec, job_vec, skills, required)
        scores.append(result['overall_score'])
    
    # Check consistency
    is_consistent = len(set(scores)) == 1
    print(f"Scoring Consistency: {'PASS' if is_consistent else 'FAIL'}")
    return is_consistent


if __name__ == "__main__":
    print("=== Performance Evaluation ===\n")
    evaluate_skill_extraction()
    evaluate_scoring_consistency()
