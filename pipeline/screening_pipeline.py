"""
Screening Pipeline Module
Main orchestration for resume screening workflow.
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import SKILLS_TAXONOMY_PATH
from config.logging_config import get_logger
from src.preprocessing import extract_text_from_pdf, clean_text, parse_resume_info
from src.feature_engineering import extract_skills, create_document_vector
from src.matching import calculate_match_score, generate_match_explanation
from src.models import Resume, JobDescription, MatchResult

logger = get_logger("pipeline")


class ScreeningPipeline:
    """Main orchestration pipeline for resume screening."""
    
    def __init__(self, skills_taxonomy_path: Optional[str] = None):
        """
        Initialize the screening pipeline.
        
        Args:
            skills_taxonomy_path: Path to skills taxonomy JSON
        """
        self.skills_taxonomy = None
        if skills_taxonomy_path and Path(skills_taxonomy_path).exists():
            from src.utils.file_handler import read_json
            self.skills_taxonomy = read_json(skills_taxonomy_path)
        
        logger.info("ScreeningPipeline initialized")
    
    def process_resume(self, pdf_path: str) -> Resume:
        """
        Process a resume PDF file.
        
        Args:
            pdf_path: Path to resume PDF
            
        Returns:
            Processed Resume object
        """
        logger.info(f"Processing resume: {pdf_path}")
        
        # Extract text
        extraction_result = extract_text_from_pdf(pdf_path)
        raw_text = extraction_result['text']
        
        # Clean text
        cleaned_text = clean_text(raw_text)
        
        # Parse structured info
        parsed_info = parse_resume_info(cleaned_text)
        
        # Extract skills
        skills = extract_skills(cleaned_text, self.skills_taxonomy)
        
        # Create vector
        vector = create_document_vector(cleaned_text)
        
        # Build Resume object
        resume = Resume(
            name=parsed_info.get('name', 'Unknown'),
            email=parsed_info.get('email'),
            phone=parsed_info.get('phone'),
            extracted_text=cleaned_text,
            skills=skills,
            vector_representation=vector,
            extraction_method=extraction_result['extraction_method'],
            num_pages=extraction_result['num_pages'],
            file_size_bytes=extraction_result['file_size_bytes'],
            source_file=pdf_path
        )
        
        logger.info(f"Resume processed: {resume.name}, {len(skills)} skills extracted")
        return resume
    
    def process_job_description(
        self,
        text: str,
        title: str = "Job Position",
        required_skills: Optional[List[Dict]] = None
    ) -> JobDescription:
        """
        Process a job description.
        
        Args:
            text: Job description text
            title: Job title
            required_skills: List of required skills with importance
            
        Returns:
            Processed JobDescription object
        """
        logger.info(f"Processing job description: {title}")
        
        # Create vector
        vector = create_document_vector(text)
        
        # Extract skills if not provided
        if required_skills is None:
            extracted = extract_skills(text, self.skills_taxonomy)
            required_skills = [
                {'skill_name': s['skill_name'], 'importance': 'preferred'}
                for s in extracted
            ]
        
        job = JobDescription(
            title=title,
            description=text,
            required_skills=required_skills,
            vector_representation=vector
        )
        
        logger.info(f"Job processed: {len(required_skills)} required skills")
        return job
    
    def match_resume_to_job(
        self,
        resume,
        job
    ) -> Dict[str, Any]:
        """
        Match a resume against a job description.
        
        Args:
            resume: Processed Resume object or dict
            job: Processed JobDescription object or dict
            
        Returns:
            Match result dictionary with explanation
        """
        # Handle dict inputs (for multi-job comparison)
        if isinstance(resume, dict):
            resume_name = resume.get('candidate', {}).get('name', 'Unknown')
            resume_vector = resume.get('vector_representation', [])
            resume_skills = resume.get('skills', [])
            resume_text = resume.get('raw_text', '')
            if resume_skills and isinstance(resume_skills[0], dict):
                resume_skill_names = [s.get('skill_name', '') for s in resume_skills]
            else:
                resume_skill_names = resume_skills
            resume_id = resume.get('resume_id', 'unknown')
        else:
            resume_name = resume.name
            resume_vector = resume.vector_representation
            resume_skill_names = resume.get_skill_names()
            resume_text = resume.extracted_text
            resume_id = resume.resume_id
        
        if isinstance(job, dict):
            job_title = job.get('title', 'Job Position')
            job_text = job.get('description', job.get('raw_text', ''))
            job_vector = job.get('vector_representation')
            required_skills = job.get('required_skills', [])
            job_id = job.get('job_id', 'unknown')
            
            # Process job if vector missing
            if job_vector is None:
                processed_job = self.process_job_description(job_text, job_title)
                job_vector = processed_job.vector_representation
                required_skills = processed_job.required_skills
                job_id = processed_job.job_id
        else:
            job_title = job.title
            job_text = job.description
            job_vector = job.vector_representation
            required_skills = job.required_skills
            job_id = job.job_id
        
        logger.info(f"Matching resume to job: {resume_name} -> {job_title}")
        
        # Calculate match score (with raw text for TF-IDF fallback)
        result = calculate_match_score(
            resume_vector=resume_vector,
            job_vector=job_vector,
            resume_skills=resume_skill_names,
            required_skills=required_skills,
            resume_text=resume_text,
            job_text=job_text
        )
        
        # Add IDs
        result['resume_id'] = resume_id
        result['job_id'] = job_id
        
        # Generate explanation
        result['explanation'] = generate_match_explanation(result)
        
        logger.info(f"Match score: {result['overall_score']:.2f} ({result['recommendation']})")
        return result

    def screen_resume(
        self,
        pdf_path: str,
        job_text: str,
        job_title: str = "Job Position"
    ) -> Dict[str, Any]:
        """
        End-to-end screening: process resume, job, and return match.
        
        Args:
            pdf_path: Path to resume PDF
            job_text: Job description text
            job_title: Job title
            
        Returns:
            Complete screening result
        """
        # Process inputs
        resume = self.process_resume(pdf_path)
        job = self.process_job_description(job_text, job_title)
        
        # Match
        match_result = self.match_resume_to_job(resume, job)
        
        return {
            'resume': resume.to_dict(),
            'job': job.to_dict(),
            'match': match_result
        }


def run_screening(
    resume_path: str,
    job_description: str,
    job_title: str = "Job Position"
) -> Dict[str, Any]:
    """
    Convenience function to run a single screening.
    
    Args:
        resume_path: Path to resume PDF
        job_description: Job description text
        job_title: Job title
        
    Returns:
        Screening result
    """
    pipeline = ScreeningPipeline()
    return pipeline.screen_resume(resume_path, job_description, job_title)


if __name__ == "__main__":
    print("Screening Pipeline ready")
    print("Usage: from pipeline.screening_pipeline import run_screening")
