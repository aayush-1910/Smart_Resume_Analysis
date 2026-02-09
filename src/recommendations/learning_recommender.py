"""
Learning Recommender Module
Generates personalized learning recommendations for missing skills.
"""
import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


# Load learning resources database
RESOURCES_PATH = Path(__file__).parent.parent.parent / "data" / "datasets" / "learning_resources.json"
SYNONYMS_PATH = Path(__file__).parent.parent.parent / "data" / "datasets" / "skill_synonyms.json"

_resources_cache = None
_synonyms_cache = None


def load_learning_resources() -> Dict:
    """Load learning resources database."""
    global _resources_cache
    if _resources_cache is None:
        if RESOURCES_PATH.exists():
            with open(RESOURCES_PATH, 'r', encoding='utf-8') as f:
                _resources_cache = json.load(f)
        else:
            _resources_cache = {}
    return _resources_cache


def load_skill_synonyms() -> Dict:
    """Load skill synonyms mapping."""
    global _synonyms_cache
    if _synonyms_cache is None:
        if SYNONYMS_PATH.exists():
            with open(SYNONYMS_PATH, 'r', encoding='utf-8') as f:
                _synonyms_cache = json.load(f)
        else:
            _synonyms_cache = {}
    return _synonyms_cache


def normalize_skill_name(skill_name: str) -> str:
    """
    Normalize skill name using synonyms mapping.
    
    Args:
        skill_name: Raw skill name
        
    Returns:
        Normalized skill name
    """
    synonyms = load_skill_synonyms()
    
    # Try exact match first
    if skill_name in synonyms:
        return synonyms[skill_name]
    
    # Try case-insensitive match
    skill_lower = skill_name.lower()
    for key, value in synonyms.items():
        if key.lower() == skill_lower:
            return value
    
    # Return original if no match
    return skill_name


def find_courses_for_skill(
    skill_name: str,
    difficulty_preference: Optional[str] = None,
    max_courses: int = 3
) -> List[Dict]:
    """
    Find courses for a skill, handling variations.
    
    Args:
        skill_name: Skill to find courses for
        difficulty_preference: Filter by difficulty (beginner/intermediate/advanced)
        max_courses: Maximum number of courses to return
        
    Returns:
        List of course dictionaries
    """
    resources = load_learning_resources()
    
    # Try normalized skill name
    normalized = normalize_skill_name(skill_name)
    
    # Try exact match
    if normalized in resources:
        courses = resources[normalized]
    elif skill_name in resources:
        courses = resources[skill_name]
    else:
        # Try case-insensitive match
        courses = None
        for key in resources:
            if key.lower() == skill_name.lower() or key.lower() == normalized.lower():
                courses = resources[key]
                break
        
        # Try partial match
        if courses is None:
            for key in resources:
                if skill_name.lower() in key.lower() or key.lower() in skill_name.lower():
                    courses = resources[key]
                    break
    
    # If no match found, return generic fallback
    if courses is None:
        return [generate_fallback_resource(skill_name)]
    
    # Filter by difficulty if specified
    if difficulty_preference:
        filtered = [c for c in courses if c.get('difficulty') == difficulty_preference]
        if filtered:
            courses = filtered
    
    # Sort by rating (highest first)
    courses = sorted(courses, key=lambda x: x.get('rating', 0), reverse=True)
    
    # Return top courses
    return courses[:max_courses]


def generate_fallback_resource(skill_name: str) -> Dict:
    """Generate generic resource for unmapped skills."""
    return {
        "title": f"Search '{skill_name}' tutorials",
        "provider": "YouTube",
        "url": f"https://www.youtube.com/results?search_query={skill_name.replace(' ', '+')}+tutorial",
        "difficulty": "varies",
        "duration": "self-paced",
        "cost": "free",
        "certificate": False,
        "rating": 4.0,
        "is_fallback": True
    }


def generate_learning_recommendations(
    missing_skills: List[Dict],
    max_skills: int = 5,
    difficulty_preference: str = "beginner",
    resume_id: Optional[str] = None,
    job_id: Optional[str] = None
) -> Dict:
    """
    Generate personalized learning recommendations for missing skills.
    
    Args:
        missing_skills: List of missing skill dicts with 'skill_name' and 'importance'
        max_skills: Maximum number of skills to include (default 5)
        difficulty_preference: Preferred difficulty level
        resume_id: Optional resume identifier
        job_id: Optional job identifier
        
    Returns:
        Learning recommendations dictionary
    """
    # Sort skills by importance
    importance_order = {'critical': 0, 'preferred': 1, 'nice-to-have': 2}
    sorted_skills = sorted(
        missing_skills,
        key=lambda x: importance_order.get(x.get('importance', 'nice-to-have'), 3)
    )
    
    # Take top N skills
    top_skills = sorted_skills[:max_skills]
    
    # Generate recommendations for each skill
    skill_recommendations = []
    total_duration_weeks = 0
    
    for skill_info in top_skills:
        skill_name = skill_info.get('skill_name', '')
        importance = skill_info.get('importance', 'preferred')
        
        courses = find_courses_for_skill(skill_name, difficulty_preference)
        
        # Add "why recommended" to each course
        for course in courses:
            if course.get('rating', 0) >= 4.8:
                course['why_recommended'] = "Highly rated by learners"
            elif course.get('cost') == 'free':
                course['why_recommended'] = "Free and comprehensive"
            elif course.get('certificate'):
                course['why_recommended'] = "Includes certificate"
            else:
                course['why_recommended'] = "Recommended for skill development"
        
        skill_recommendations.append({
            'skill_name': skill_name,
            'importance': importance,
            'current_proficiency': 'none',
            'recommended_courses': courses
        })
        
        # Estimate duration
        if courses and not courses[0].get('is_fallback'):
            duration = courses[0].get('duration', '')
            if 'week' in duration.lower():
                try:
                    weeks = int(''.join(filter(str.isdigit, duration.split()[0])))
                    total_duration_weeks += weeks
                except:
                    total_duration_weeks += 4
            elif 'month' in duration.lower():
                try:
                    months = int(''.join(filter(str.isdigit, duration.split()[0])))
                    total_duration_weeks += months * 4
                except:
                    total_duration_weeks += 4
            else:
                total_duration_weeks += 2
    
    # Generate learning path milestones
    milestones = generate_learning_milestones(skill_recommendations)
    
    # Format total duration
    if total_duration_weeks <= 4:
        estimated_time = "1 month"
    elif total_duration_weeks <= 12:
        estimated_time = f"{total_duration_weeks // 4}-{(total_duration_weeks // 4) + 1} months"
    else:
        estimated_time = f"{total_duration_weeks // 4} months"
    
    return {
        'learning_plan_id': str(uuid.uuid4()),
        'resume_id': resume_id or str(uuid.uuid4()),
        'job_id': job_id or str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'total_skills_to_learn': len(skill_recommendations),
        'estimated_total_time': estimated_time,
        'skills': skill_recommendations,
        'learning_path_milestones': milestones
    }


def generate_learning_milestones(skill_recommendations: List[Dict]) -> List[Dict]:
    """Generate month-by-month learning milestones."""
    milestones = []
    
    for i, skill in enumerate(skill_recommendations):
        skill_name = skill['skill_name']
        courses = skill.get('recommended_courses', [])
        
        if courses:
            course_titles = [c['title'] for c in courses[:1]]
            
            milestone = {
                'month': i + 1,
                'focus': f"{skill_name} fundamentals",
                'courses': course_titles,
                'expected_outcome': f"Build foundational knowledge in {skill_name}"
            }
            
            # Customize outcome based on skill type
            skill_lower = skill_name.lower()
            if any(kw in skill_lower for kw in ['python', 'javascript', 'java', 'programming']):
                milestone['expected_outcome'] = f"Write basic {skill_name} programs"
            elif any(kw in skill_lower for kw in ['machine learning', 'deep learning', 'ml', 'ai']):
                milestone['expected_outcome'] = "Build simple ML models"
            elif any(kw in skill_lower for kw in ['react', 'angular', 'vue', 'frontend']):
                milestone['expected_outcome'] = "Create interactive web components"
            elif any(kw in skill_lower for kw in ['docker', 'kubernetes', 'devops', 'aws']):
                milestone['expected_outcome'] = "Deploy applications to cloud"
            elif any(kw in skill_lower for kw in ['communication', 'leadership', 'teamwork']):
                milestone['expected_outcome'] = f"Apply {skill_name} skills in workplace"
            
            milestones.append(milestone)
    
    return milestones


def get_skill_coverage_stats() -> Dict:
    """Get statistics about skill coverage in the database."""
    resources = load_learning_resources()
    
    total_skills = len(resources)
    total_courses = sum(len(courses) for courses in resources.values())
    
    # Count by difficulty
    difficulty_counts = {'beginner': 0, 'intermediate': 0, 'advanced': 0}
    free_courses = 0
    certified_courses = 0
    
    for courses in resources.values():
        for course in courses:
            difficulty = course.get('difficulty', 'beginner')
            if difficulty in difficulty_counts:
                difficulty_counts[difficulty] += 1
            if course.get('cost') in ['free', 'free to audit']:
                free_courses += 1
            if course.get('certificate'):
                certified_courses += 1
    
    return {
        'total_skills': total_skills,
        'total_courses': total_courses,
        'difficulty_distribution': difficulty_counts,
        'free_courses': free_courses,
        'certified_courses': certified_courses
    }
