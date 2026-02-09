"""
Command Line Interface for AI Resume Screener
"""
import argparse
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AI Resume Screener - Match resumes to job descriptions'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Screen command
    screen_parser = subparsers.add_parser('screen', help='Screen a resume against a job')
    screen_parser.add_argument('--resume', '-r', required=True, help='Path to resume PDF')
    screen_parser.add_argument('--job', '-j', required=True, help='Job description text or file path')
    screen_parser.add_argument('--title', '-t', default='Job Position', help='Job title')
    screen_parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract text from PDF')
    extract_parser.add_argument('--file', '-f', required=True, help='Path to PDF file')
    
    # Skills command
    skills_parser = subparsers.add_parser('skills', help='Extract skills from text')
    skills_parser.add_argument('--text', '-t', help='Text to analyze')
    skills_parser.add_argument('--file', '-f', help='File containing text')
    
    args = parser.parse_args()
    
    if args.command == 'screen':
        run_screen(args)
    elif args.command == 'extract':
        run_extract(args)
    elif args.command == 'skills':
        run_skills(args)
    else:
        parser.print_help()


def run_screen(args):
    """Run resume screening."""
    from pipeline.screening_pipeline import ScreeningPipeline
    
    # Read job description
    job_text = args.job
    if Path(args.job).exists():
        job_text = Path(args.job).read_text()
    
    print(f"📄 Processing resume: {args.resume}")
    print(f"📋 Job: {args.title}")
    
    pipeline = ScreeningPipeline()
    result = pipeline.screen_resume(args.resume, job_text, args.title)
    
    # Display result
    match = result['match']
    print(f"\n{'='*50}")
    print(f"📊 MATCH RESULT")
    print(f"{'='*50}")
    print(f"Overall Score: {match['overall_score']:.0%}")
    print(f"Recommendation: {match['recommendation'].replace('-', ' ').title()}")
    print(f"\nSkill Match: {match['subscores']['skill_match']:.0%}")
    print(f"Semantic Similarity: {match['subscores']['semantic_similarity']:.0%}")
    
    if match['matched_skills']:
        print(f"\n✓ Matched Skills: {', '.join(match['matched_skills'])}")
    
    if match['missing_skills']:
        missing = [s['skill_name'] for s in match['missing_skills']]
        print(f"✗ Missing Skills: {', '.join(missing)}")
    
    # Save output if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {args.output}")


def run_extract(args):
    """Run text extraction."""
    from src.preprocessing import extract_text_from_pdf
    
    result = extract_text_from_pdf(args.file)
    print(f"Pages: {result['num_pages']}")
    print(f"Method: {result['extraction_method']}")
    print(f"\n{'='*50}")
    print("EXTRACTED TEXT:")
    print(f"{'='*50}")
    print(result['text'][:2000])
    if len(result['text']) > 2000:
        print(f"\n... (truncated, {len(result['text'])} total characters)")


def run_skills(args):
    """Run skill extraction."""
    from src.feature_engineering import extract_skills
    
    text = args.text
    if args.file:
        text = Path(args.file).read_text()
    
    if not text:
        print("Error: Provide --text or --file")
        return
    
    skills = extract_skills(text)
    print(f"Found {len(skills)} skills:\n")
    
    for skill in sorted(skills, key=lambda x: (-x['confidence'], x['skill_name'])):
        print(f"  {skill['skill_name']} ({skill['category']}): {skill['confidence']:.0%}")


if __name__ == '__main__':
    main()
