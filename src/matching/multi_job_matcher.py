"""
Multi-Job Matcher Module
Compares one resume against multiple job descriptions.
"""
import uuid
from typing import Dict, List
from datetime import datetime


def compare_resume_to_jobs(
    resume_data: Dict,
    job_descriptions: List[Dict],
    max_jobs: int = 5
) -> Dict:
    """
    Compare one resume against multiple job descriptions.
    
    Args:
        resume_data: Processed resume from existing pipeline
        job_descriptions: List of 2-5 job dictionaries with title, description, required_skills
        max_jobs: Maximum number of jobs to compare (default 5)
        
    Returns:
        Comparison results with ranked jobs
        
    Raises:
        ValueError: If job count is out of valid range (2-5)
    """
    # Validate input
    if len(job_descriptions) < 2:
        raise ValueError("Minimum 2 jobs required for comparison")
    if len(job_descriptions) > max_jobs:
        raise ValueError(f"Maximum {max_jobs} jobs allowed, got {len(job_descriptions)}")
    
    # Validate each job has required fields
    for i, job in enumerate(job_descriptions):
        if not job.get('title'):
            raise ValueError(f"Job {i+1} missing 'title' field")
        if not job.get('description'):
            raise ValueError(f"Job {i+1} missing 'description' field")
    
    # Import here to avoid circular imports
    from pipeline.screening_pipeline import ScreeningPipeline
    
    pipeline = ScreeningPipeline()
    results = []
    
    # Process each job sequentially
    for job in job_descriptions:
        job_id = job.get('job_id') or str(uuid.uuid4())
        
        try:
            # Use existing scoring function
            match_result = pipeline.match_resume_to_job(resume_data, job)
            
            results.append({
                'job_id': job_id,
                'job_title': job.get('title', ''),
                'job_company': job.get('company'),
                'overall_score': match_result.get('overall_score', 0),
                'subscores': match_result.get('subscores', {}),
                'matched_skills': match_result.get('matched_skills', []),
                'missing_skills': match_result.get('missing_skills', []),
                'recommendation': match_result.get('recommendation', 'unknown')
            })
        except Exception as e:
            # Log error but continue with other jobs
            results.append({
                'job_id': job_id,
                'job_title': job.get('title', ''),
                'job_company': job.get('company'),
                'overall_score': 0,
                'subscores': {},
                'matched_skills': [],
                'missing_skills': [],
                'recommendation': 'error',
                'error': str(e)
            })
    
    # Sort by overall_score descending
    results.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
    
    # Add ranks
    for i, result in enumerate(results):
        result['rank'] = i + 1
    
    # Build response
    best_match = results[0] if results else None
    
    return {
        'comparison_id': str(uuid.uuid4()),
        'resume_id': resume_data.get('resume_id') or str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'num_jobs_compared': len(results),
        'best_match': {
            'rank': 1,
            'job_title': best_match.get('job_title', '') if best_match else '',
            'overall_score': best_match.get('overall_score', 0) if best_match else 0
        } if best_match else None,
        'results': results
    }


def format_comparison_table(comparison_result: Dict) -> str:
    """
    Format comparison results as a text table for display.
    
    Args:
        comparison_result: Result from compare_resume_to_jobs
        
    Returns:
        Formatted table string
    """
    results = comparison_result.get('results', [])
    
    if not results:
        return "No comparison results available."
    
    # Header
    lines = [
        "=" * 80,
        "MULTI-JOB COMPARISON RESULTS",
        "=" * 80,
        f"{'Rank':<6}{'Job Title':<30}{'Score':<10}{'Match':<15}{'Skills':<10}",
        "-" * 80
    ]
    
    # Rows
    for result in results:
        rank = result.get('rank', '-')
        title = result.get('job_title', '')[:28]
        score = f"{result.get('overall_score', 0):.0%}"
        recommendation = result.get('recommendation', 'unknown').replace('-', ' ').title()
        matched = len(result.get('matched_skills', []))
        
        lines.append(f"{rank:<6}{title:<30}{score:<10}{recommendation:<15}{matched:<10}")
    
    lines.append("=" * 80)
    
    return "\n".join(lines)


def get_best_match_details(comparison_result: Dict) -> Dict:
    """
    Get detailed breakdown of the best matching job.
    
    Args:
        comparison_result: Result from compare_resume_to_jobs
        
    Returns:
        Detailed best match information
    """
    results = comparison_result.get('results', [])
    
    if not results:
        return {}
    
    best = results[0]  # Already sorted
    
    return {
        'job_title': best.get('job_title', ''),
        'job_company': best.get('job_company'),
        'overall_score': best.get('overall_score', 0),
        'skill_match_score': best.get('subscores', {}).get('skill_match', 0),
        'semantic_similarity': best.get('subscores', {}).get('semantic_similarity', 0),
        'matched_skills': best.get('matched_skills', []),
        'missing_skills': best.get('missing_skills', []),
        'recommendation': best.get('recommendation', ''),
        'advantage_over_second': (
            results[0].get('overall_score', 0) - results[1].get('overall_score', 0)
            if len(results) > 1 else 0
        )
    }
