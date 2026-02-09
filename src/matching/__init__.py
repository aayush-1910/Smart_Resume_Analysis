"""Matching module for resume-job similarity scoring."""
from .similarity_scorer import calculate_match_score
from .classifier import classify_match
from .explainer import generate_match_explanation
from .improvement_analyzer import generate_improvement_suggestions
from .multi_job_matcher import compare_resume_to_jobs
