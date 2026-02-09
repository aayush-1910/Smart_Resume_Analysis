"""
Resume Improvement Analyzer Module
Analyzes resume quality and generates actionable improvement suggestions.
"""
import re
import uuid
from typing import Dict, List, Optional
from datetime import datetime


def generate_improvement_suggestions(
    resume_data: Dict,
    job_data: Dict,
    match_result: Dict
) -> Dict:
    """
    Generate improvement suggestions for a resume based on job match.
    
    Args:
        resume_data: Processed resume dictionary
        job_data: Job description dictionary
        match_result: Match result from scoring pipeline
        
    Returns:
        Structured suggestions object
    """
    suggestions = []
    positive_points = []
    
    # Extract data
    resume_text = resume_data.get('raw_text', '')
    candidate = resume_data.get('candidate', {})
    resume_skills = set(s.lower() for s in resume_data.get('skills', []))
    
    matched_skills = match_result.get('matched_skills', [])
    missing_skills = match_result.get('missing_skills', [])
    
    # 1. Analyze Missing Critical Skills
    critical_missing = [s for s in missing_skills if s.get('importance') == 'critical']
    if critical_missing:
        skill_names = [s.get('skill_name', '') for s in critical_missing[:5]]
        suggestions.append({
            'category': 'missing_critical_skills',
            'priority': 'high',
            'title': f"Add Critical Skills: {', '.join(skill_names[:3])}",
            'description': f"This job requires {', '.join(skill_names)} as critical skills, but they're not clearly mentioned in your resume.",
            'action_items': [
                "Add a dedicated 'Technical Skills' or 'Skills' section if missing",
                f"List your experience with {skill_names[0] if skill_names else 'these technologies'} in your projects",
                "Include these skills in your work experience descriptions where applicable"
            ],
            'impact': f"Adding these could improve your match score by ~{min(25, len(skill_names) * 5)}%"
        })
    
    # 2. Analyze Missing Keywords
    missing_keywords = analyze_missing_keywords(resume_text, job_data)
    if missing_keywords:
        suggestions.append({
            'category': 'missing_keywords',
            'priority': 'medium',
            'title': f"Add Key Terms: {', '.join(missing_keywords[:3])}",
            'description': "Important keywords from the job description are missing from your resume.",
            'action_items': [
                f"Incorporate '{missing_keywords[0]}' in relevant sections" if missing_keywords else "Review job keywords",
                "Mirror the language used in the job description",
                "Add industry-specific terminology where applicable"
            ],
            'impact': "Better keyword alignment improves ATS matching"
        })
    
    # 3. Analyze Formatting Issues
    formatting_issues = analyze_formatting(resume_text, candidate)
    suggestions.extend(formatting_issues)
    
    # 4. Analyze Content Gaps
    content_gaps = analyze_content_gaps(resume_text)
    suggestions.extend(content_gaps)
    
    # 5. Analyze ATS Compatibility
    ats_issues = analyze_ats_compatibility(resume_data)
    suggestions.extend(ats_issues)
    
    # Generate Positive Points
    positive_points = generate_positive_points(resume_data, match_result, resume_text)
    
    # Calculate Quality Score
    quality_score = calculate_quality_score(resume_text, candidate, resume_skills, matched_skills)
    
    # Sort suggestions by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
    
    return {
        'suggestion_id': str(uuid.uuid4()),
        'resume_id': resume_data.get('resume_id', str(uuid.uuid4())),
        'job_id': job_data.get('job_id', str(uuid.uuid4())),
        'timestamp': datetime.now().isoformat(),
        'overall_resume_quality_score': quality_score,
        'suggestions': suggestions,
        'positive_points': positive_points
    }


def analyze_missing_keywords(resume_text: str, job_data: Dict) -> List[str]:
    """Extract keywords from job that are missing in resume."""
    job_text = job_data.get('description', '') or job_data.get('raw_text', '')
    
    # Action verbs commonly used in job descriptions
    action_verbs = [
        'develop', 'design', 'implement', 'manage', 'lead', 'create',
        'analyze', 'build', 'collaborate', 'optimize', 'maintain'
    ]
    
    # Extract meaningful words from job (3+ chars, not common)
    common_words = {'the', 'and', 'for', 'with', 'you', 'will', 'are', 'this', 'that', 'have', 'from'}
    job_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_text.lower()))
    job_words -= common_words
    
    resume_lower = resume_text.lower()
    
    # Find missing keywords
    missing = []
    for word in job_words:
        if word not in resume_lower and len(word) > 4:
            missing.append(word)
    
    # Prioritize action verbs
    missing_actions = [w for w in action_verbs if w in job_text.lower() and w not in resume_lower]
    
    return (missing_actions + missing)[:15]


def analyze_formatting(resume_text: str, candidate: Dict) -> List[Dict]:
    """Analyze formatting and contact information issues."""
    issues = []
    
    # Check contact info
    has_email = bool(candidate.get('email'))
    has_phone = bool(candidate.get('phone'))
    has_name = bool(candidate.get('name') and candidate.get('name') != 'Unknown')
    
    if not has_email or not has_phone or not has_name:
        missing_contact = []
        if not has_name:
            missing_contact.append('name')
        if not has_email:
            missing_contact.append('email')
        if not has_phone:
            missing_contact.append('phone')
        
        issues.append({
            'category': 'formatting',
            'priority': 'high',
            'title': f"Add Missing Contact Info: {', '.join(missing_contact)}",
            'description': "Essential contact information is missing or not properly formatted.",
            'action_items': [
                "Include your full name at the top of the resume",
                "Add a professional email address",
                "Include a phone number with area code"
            ],
            'impact': "Recruiters cannot contact you without complete contact information"
        })
    
    # Check resume length
    char_count = len(resume_text)
    if char_count < 500:
        issues.append({
            'category': 'formatting',
            'priority': 'high',
            'title': "Resume Too Short",
            'description': f"Your resume has only {char_count} characters. This may indicate missing content or extraction issues.",
            'action_items': [
                "Expand your work experience descriptions",
                "Add more details about projects and achievements",
                "Include education, skills, and certifications sections"
            ],
            'impact': "Short resumes lack the detail needed to assess qualifications"
        })
    elif char_count > 30000:
        issues.append({
            'category': 'formatting',
            'priority': 'medium',
            'title': "Resume May Be Too Long",
            'description': f"Your resume has {char_count} characters, which may be too lengthy.",
            'action_items': [
                "Focus on the most recent 10-15 years of experience",
                "Remove outdated or irrelevant information",
                "Use concise bullet points instead of paragraphs"
            ],
            'impact': "Long resumes may not be fully read by recruiters"
        })
    
    # Check for section headers
    section_keywords = ['experience', 'education', 'skills', 'summary', 'objective', 'projects']
    found_sections = sum(1 for kw in section_keywords if kw in resume_text.lower())
    
    if found_sections < 2:
        issues.append({
            'category': 'formatting',
            'priority': 'medium',
            'title': "Add Clear Section Headers",
            'description': "Your resume may lack clear section organization.",
            'action_items': [
                "Add 'Work Experience' or 'Professional Experience' section",
                "Include 'Education' section with degrees",
                "Add 'Skills' or 'Technical Skills' section"
            ],
            'impact': "Well-organized resumes are easier to scan quickly"
        })
    
    return issues


def analyze_content_gaps(resume_text: str) -> List[Dict]:
    """Analyze content gaps in the resume."""
    gaps = []
    text_lower = resume_text.lower()
    
    # Check for education
    education_keywords = ['degree', 'bachelor', 'master', 'phd', 'university', 'college', 'diploma', 'b.s.', 'b.a.', 'm.s.', 'm.a.']
    has_education = any(kw in text_lower for kw in education_keywords)
    
    if not has_education:
        gaps.append({
            'category': 'content_gaps',
            'priority': 'medium',
            'title': "Add Education Section",
            'description': "No education credentials were detected in your resume.",
            'action_items': [
                "Add your highest degree and institution",
                "Include graduation year (optional if >15 years)",
                "Mention relevant coursework or honors if applicable"
            ],
            'impact': "Education is often a basic requirement filter"
        })
    
    # Check for experience indicators
    experience_keywords = ['worked', 'managed', 'developed', 'led', 'created', 'company', 'responsibilities']
    has_experience = any(kw in text_lower for kw in experience_keywords)
    
    if not has_experience:
        gaps.append({
            'category': 'content_gaps',
            'priority': 'medium',
            'title': "Expand Work Experience Details",
            'description': "Your resume may lack detailed work experience descriptions.",
            'action_items': [
                "Use action verbs to describe your accomplishments",
                "Include job titles, company names, and dates",
                "Describe your responsibilities and achievements"
            ],
            'impact': "Work experience is the most important section for most roles"
        })
    
    # Check for quantifiable achievements
    has_numbers = bool(re.search(r'\b\d+%|\$\d+|\d+\s*(million|thousand|users|customers|projects)', text_lower))
    
    if not has_numbers:
        gaps.append({
            'category': 'content_gaps',
            'priority': 'medium',
            'title': "Add Quantifiable Achievements",
            'description': "Your resume lacks numbers and metrics. Recruiters prefer measurable impact.",
            'action_items': [
                "Add metrics like 'Improved performance by 20%'",
                "Quantify project outcomes: 'Processed 1M+ records'",
                "Include team size, budget, or timeline numbers"
            ],
            'impact': "Makes your resume more compelling and credible"
        })
    
    return gaps


def analyze_ats_compatibility(resume_data: Dict) -> List[Dict]:
    """Analyze ATS compatibility issues."""
    issues = []
    
    # Check file size (if available)
    file_size = resume_data.get('file_size_kb', 0)
    if file_size > 5000:  # 5MB
        issues.append({
            'category': 'ats_compatibility',
            'priority': 'low',
            'title': "File Size Warning",
            'description': f"Your resume is {file_size/1000:.1f}MB, which may be too large for some ATS systems.",
            'action_items': [
                "Compress images if any are included",
                "Consider using a simpler format",
                "Remove unnecessary graphics or design elements"
            ],
            'impact': "Large files may fail to upload or process correctly"
        })
    
    # Check for potential parsing issues
    resume_text = resume_data.get('raw_text', '')
    
    # Check for tables (indicated by excessive whitespace patterns)
    if resume_text.count('\t') > 20 or resume_text.count('    ') > 30:
        issues.append({
            'category': 'ats_compatibility',
            'priority': 'low',
            'title': "Consider Simpler Formatting",
            'description': "Your resume may have complex formatting (tables/columns) that ATS may not parse correctly.",
            'action_items': [
                "Use a single-column layout for better ATS compatibility",
                "Avoid tables and text boxes",
                "Use standard bullet points instead of custom symbols"
            ],
            'impact': "Complex layouts can cause ATS parsing errors"
        })
    
    return issues


def calculate_quality_score(
    resume_text: str,
    candidate: Dict,
    resume_skills: set,
    matched_skills: List
) -> float:
    """
    Calculate overall resume quality score (0-100).
    
    Base score: 50
    + Has email: +10
    + Has phone: +5
    + 500-5000 chars: +10
    + Has education keywords: +10
    + Has experience keywords: +10
    + Has quantifiable achievements: +10
    + Good skill balance: +5
    """
    score = 50
    text_lower = resume_text.lower()
    
    # Contact info
    if candidate.get('email'):
        score += 10
    if candidate.get('phone'):
        score += 5
    
    # Length
    char_count = len(resume_text)
    if 500 <= char_count <= 5000:
        score += 10
    elif 5000 < char_count <= 15000:
        score += 7
    elif char_count > 15000:
        score += 3
    
    # Education
    education_keywords = ['degree', 'bachelor', 'master', 'phd', 'university', 'college']
    if any(kw in text_lower for kw in education_keywords):
        score += 10
    
    # Experience
    experience_keywords = ['worked', 'managed', 'developed', 'led', 'created', 'responsible']
    if any(kw in text_lower for kw in experience_keywords):
        score += 10
    
    # Quantifiable achievements
    if re.search(r'\b\d+%|\$\d+|\d+\s*(million|thousand|users|projects)', text_lower):
        score += 10
    
    # Skill balance (has both technical and soft skills)
    soft_skills = {'communication', 'leadership', 'teamwork', 'problem solving', 'collaboration'}
    has_soft = any(skill in soft_skills for skill in resume_skills)
    has_technical = len(resume_skills - soft_skills) > 0
    if has_soft and has_technical:
        score += 5
    
    return min(100, score)


def generate_positive_points(resume_data: Dict, match_result: Dict, resume_text: str) -> List[str]:
    """Generate positive feedback about the resume."""
    positive = []
    text_lower = resume_text.lower()
    
    # Matched skills
    matched_count = len(match_result.get('matched_skills', []))
    if matched_count > 0:
        positive.append(f"Strong skill alignment: {matched_count} skills match the job requirements")
    
    # Overall score
    overall_score = match_result.get('overall_score', 0)
    if overall_score >= 0.75:
        positive.append("Excellent overall match for this position")
    elif overall_score >= 0.55:
        positive.append("Good foundation for this role with room to grow")
    
    # Contact info
    candidate = resume_data.get('candidate', {})
    if candidate.get('email') and candidate.get('phone'):
        positive.append("Complete contact information provided")
    
    # Length
    if 1000 <= len(resume_text) <= 10000:
        positive.append("Well-structured resume length")
    
    # Experience
    if any(kw in text_lower for kw in ['years', 'experience', 'senior', 'lead', 'manager']):
        positive.append("Demonstrates relevant professional experience")
    
    # Quantifiable
    if re.search(r'\b\d+%|\$\d+|\d+\s*(million|thousand|users)', text_lower):
        positive.append("Includes quantifiable achievements")
    
    # Limit to 5 points
    return positive[:5]


def get_improvement_summary(suggestions_result: Dict) -> str:
    """Generate a brief text summary of improvement suggestions."""
    suggestions = suggestions_result.get('suggestions', [])
    quality_score = suggestions_result.get('overall_resume_quality_score', 50)
    
    high_priority = [s for s in suggestions if s.get('priority') == 'high']
    medium_priority = [s for s in suggestions if s.get('priority') == 'medium']
    
    lines = [
        f"Resume Quality Score: {quality_score}/100",
        "",
        f"Total Suggestions: {len(suggestions)}",
        f"  - High Priority: {len(high_priority)}",
        f"  - Medium Priority: {len(medium_priority)}",
        ""
    ]
    
    if high_priority:
        lines.append("Top Priority Actions:")
        for s in high_priority[:3]:
            lines.append(f"  • {s.get('title', '')}")
    
    return "\n".join(lines)
