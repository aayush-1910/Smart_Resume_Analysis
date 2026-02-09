"""
Batch Processing Module
Process multiple resumes against a single job description.
"""
import uuid
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable
from datetime import datetime


def batch_process_resumes(
    resume_files: List[str],
    job_data: Dict,
    max_resumes: int = 10,
    progress_callback: Optional[Callable[[int, int, str], None]] = None
) -> Dict:
    """
    Process multiple resumes against a single job description.
    
    Args:
        resume_files: List of file paths to PDF resumes
        job_data: Single job description dictionary
        max_resumes: Maximum number of resumes to process (default 10)
        progress_callback: Optional callback(current, total, status) for progress updates
        
    Returns:
        Batch results with all candidates ranked
        
    Raises:
        ValueError: If resume count is out of valid range (2-10)
    """
    # Validate input
    if len(resume_files) < 2:
        raise ValueError("Minimum 2 resumes required for batch processing")
    if len(resume_files) > max_resumes:
        raise ValueError(f"Maximum {max_resumes} resumes allowed, got {len(resume_files)}")
    
    # Validate job data
    if not job_data.get('description') and not job_data.get('raw_text'):
        raise ValueError("Job description is required")
    
    # Check total file size
    total_size_bytes = 0
    for file_path in resume_files:
        path = Path(file_path)
        if path.exists():
            total_size_bytes += path.stat().st_size
    
    max_total_size = 50 * 1024 * 1024  # 50MB
    if total_size_bytes > max_total_size:
        raise ValueError(f"Total file size exceeds {max_total_size // (1024*1024)}MB limit")
    
    # Import pipeline
    from pipeline.screening_pipeline import ScreeningPipeline
    
    pipeline = ScreeningPipeline()
    
    results = []
    failed_resumes = []
    start_time = time.time()
    
    job_title = job_data.get('title', 'Job Position')
    
    # Process each resume sequentially
    for i, file_path in enumerate(resume_files):
        filename = Path(file_path).name
        
        # Progress callback
        if progress_callback:
            progress_callback(i + 1, len(resume_files), f"Processing: {filename}")
        
        try:
            # Validate file exists and is PDF
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            if path.suffix.lower() != '.pdf':
                raise ValueError(f"Invalid file type: {path.suffix}")
            
            # Process through pipeline
            result = pipeline.screen_resume(
                resume_path=str(path),
                job_description=job_data.get('description', job_data.get('raw_text', '')),
                job_title=job_title
            )
            
            resume_info = result.get('resume', {})
            match_info = result.get('match', {})
            candidate = resume_info.get('candidate', {})
            
            results.append({
                'resume_id': str(uuid.uuid4()),
                'filename': filename,
                'candidate_name': candidate.get('name', 'Unknown'),
                'candidate_email': candidate.get('email'),
                'overall_score': match_info.get('overall_score', 0),
                'subscores': match_info.get('subscores', {}),
                'matched_skills': match_info.get('matched_skills', []),
                'missing_skills': match_info.get('missing_skills', []),
                'recommendation': match_info.get('recommendation', 'unknown')
            })
            
        except FileNotFoundError as e:
            failed_resumes.append({
                'filename': filename,
                'error_code': 'FILE_NOT_FOUND',
                'error_message': str(e)
            })
        except ValueError as e:
            failed_resumes.append({
                'filename': filename,
                'error_code': 'INVALID_FILE',
                'error_message': str(e)
            })
        except Exception as e:
            error_code = 'PDF_CORRUPTED' if 'pdf' in str(e).lower() else 'PROCESSING_ERROR'
            failed_resumes.append({
                'filename': filename,
                'error_code': error_code,
                'error_message': str(e)
            })
    
    # Sort results by overall_score descending
    results.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
    
    # Add ranks
    for i, result in enumerate(results):
        result['rank'] = i + 1
    
    processing_time = time.time() - start_time
    
    return {
        'batch_id': str(uuid.uuid4()),
        'job_id': job_data.get('job_id', str(uuid.uuid4())),
        'job_title': job_title,
        'timestamp': datetime.now().isoformat(),
        'total_resumes_uploaded': len(resume_files),
        'successfully_processed': len(results),
        'failed_resumes': failed_resumes,
        'processing_time_seconds': round(processing_time, 2),
        'results': results
    }


def format_batch_results_table(batch_result: Dict) -> str:
    """
    Format batch results as a text table.
    
    Args:
        batch_result: Result from batch_process_resumes
        
    Returns:
        Formatted table string
    """
    results = batch_result.get('results', [])
    
    if not results:
        return "No results to display."
    
    lines = [
        "=" * 90,
        f"BATCH PROCESSING RESULTS - {batch_result.get('job_title', 'Job')}",
        "=" * 90,
        f"Processed: {batch_result.get('successfully_processed', 0)} | Failed: {len(batch_result.get('failed_resumes', []))} | Time: {batch_result.get('processing_time_seconds', 0):.1f}s",
        "-" * 90,
        f"{'Rank':<6}{'Candidate':<25}{'Email':<30}{'Score':<10}{'Match':<15}",
        "-" * 90
    ]
    
    for result in results:
        rank = result.get('rank', '-')
        name = (result.get('candidate_name', 'Unknown')[:23])
        email = (result.get('candidate_email', 'N/A') or 'N/A')[:28]
        score = f"{result.get('overall_score', 0):.0%}"
        recommendation = result.get('recommendation', 'unknown').replace('-', ' ').title()
        
        lines.append(f"{rank:<6}{name:<25}{email:<30}{score:<10}{recommendation:<15}")
    
    lines.append("=" * 90)
    
    # Add failed resumes if any
    failed = batch_result.get('failed_resumes', [])
    if failed:
        lines.append("\nFailed to Process:")
        for f in failed:
            lines.append(f"  - {f.get('filename', '')}: {f.get('error_message', '')}")
    
    return "\n".join(lines)


def export_batch_results_csv(batch_result: Dict) -> str:
    """
    Export batch results as CSV string.
    
    Args:
        batch_result: Result from batch_process_resumes
        
    Returns:
        CSV formatted string
    """
    results = batch_result.get('results', [])
    
    # CSV header
    lines = ["Rank,Candidate Name,Email,Filename,Overall Score,Skill Match,Semantic Similarity,Recommendation,Matched Skills Count,Missing Skills Count"]
    
    for result in results:
        row = [
            str(result.get('rank', '')),
            f'"{result.get("candidate_name", "Unknown")}"',
            f'"{result.get("candidate_email", "") or ""}"',
            f'"{result.get("filename", "")}"',
            f'{result.get("overall_score", 0):.2%}',
            f'{result.get("subscores", {}).get("skill_match", 0):.2%}',
            f'{result.get("subscores", {}).get("semantic_similarity", 0):.2%}',
            result.get('recommendation', 'unknown'),
            str(len(result.get('matched_skills', []))),
            str(len(result.get('missing_skills', [])))
        ]
        lines.append(','.join(row))
    
    return '\n'.join(lines)


def get_top_candidates(batch_result: Dict, top_n: int = 3) -> List[Dict]:
    """
    Get the top N candidates from batch results.
    
    Args:
        batch_result: Result from batch_process_resumes
        top_n: Number of top candidates to return
        
    Returns:
        List of top candidate results
    """
    results = batch_result.get('results', [])
    return results[:top_n]


def get_batch_statistics(batch_result: Dict) -> Dict:
    """
    Get statistics about the batch processing results.
    
    Args:
        batch_result: Result from batch_process_resumes
        
    Returns:
        Statistics dictionary
    """
    results = batch_result.get('results', [])
    
    if not results:
        return {
            'total_processed': 0,
            'average_score': 0,
            'strong_matches': 0,
            'good_matches': 0,
            'weak_matches': 0,
            'no_matches': 0
        }
    
    scores = [r.get('overall_score', 0) for r in results]
    recommendations = [r.get('recommendation', '') for r in results]
    
    return {
        'total_processed': len(results),
        'average_score': sum(scores) / len(scores) if scores else 0,
        'highest_score': max(scores) if scores else 0,
        'lowest_score': min(scores) if scores else 0,
        'strong_matches': recommendations.count('strong-match'),
        'good_matches': recommendations.count('good-match'),
        'weak_matches': recommendations.count('weak-match'),
        'no_matches': recommendations.count('no-match'),
        'failed_count': len(batch_result.get('failed_resumes', []))
    }
