"""
Batch Processing Script
Process multiple resumes against a job description.
"""
import os
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import ScreeningPipeline


def process_batch(resume_dir: str, job_description: str, output_file: str = None):
    """
    Process all PDF resumes in a directory.
    
    Args:
        resume_dir: Directory containing resume PDFs
        job_description: Job description text
        output_file: Optional output file for results
    """
    pipeline = ScreeningPipeline()
    results = []
    
    resume_path = Path(resume_dir)
    pdf_files = list(resume_path.glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} resume(s) to process")
    
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        try:
            result = pipeline.screen_resume(str(pdf_file), job_description)
            result['filename'] = pdf_file.name
            results.append(result)
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")
            results.append({
                'filename': pdf_file.name,
                'error': str(e)
            })
    
    # Sort by score
    results.sort(
        key=lambda x: x.get('match', {}).get('overall_score', 0),
        reverse=True
    )
    
    # Output results
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to: {output_file}")
    
    # Print summary
    print("\n=== BATCH RESULTS ===")
    for r in results:
        if 'error' in r:
            print(f"❌ {r['filename']}: {r['error']}")
        else:
            score = r['match']['overall_score']
            rec = r['match']['recommendation']
            print(f"{'🟢' if score >= 0.55 else '🔴'} {r['filename']}: {score:.0%} ({rec})")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch process resumes")
    parser.add_argument("--dir", "-d", required=True, help="Resume directory")
    parser.add_argument("--job", "-j", required=True, help="Job description file or text")
    parser.add_argument("--output", "-o", help="Output JSON file")
    
    args = parser.parse_args()
    
    job_text = args.job
    if Path(args.job).exists():
        job_text = Path(args.job).read_text()
    
    process_batch(args.dir, job_text, args.output)
