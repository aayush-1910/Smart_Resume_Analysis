"""
Explainer Module
Generates human-readable explanations for match results.
"""
from typing import Dict, List, Any

from config.logging_config import get_logger

logger = get_logger("explainer")


def generate_match_explanation(match_result: Dict[str, Any]) -> str:
    """
    Generate a human-readable explanation of the match result.
    
    Args:
        match_result: Match result dictionary
        
    Returns:
        Formatted explanation string
    """
    overall_score = match_result.get('overall_score', 0)
    recommendation = match_result.get('recommendation', 'unknown')
    subscores = match_result.get('subscores', {})
    matched_skills = match_result.get('matched_skills', [])
    missing_skills = match_result.get('missing_skills', [])
    
    # Build explanation
    lines = []
    
    # Overall assessment
    lines.append(f"## Match Assessment: {recommendation.replace('-', ' ').title()}")
    lines.append(f"**Overall Score: {overall_score:.0%}**")
    lines.append("")
    
    # Score breakdown
    lines.append("### Score Breakdown")
    skill_score = subscores.get('skill_match', 0)
    semantic_score = subscores.get('semantic_similarity', 0)
    lines.append(f"- Skill Match: {skill_score:.0%}")
    lines.append(f"- Semantic Similarity: {semantic_score:.0%}")
    lines.append("")
    
    # Matched skills
    if matched_skills:
        lines.append("### ✓ Matched Skills")
        for skill in matched_skills:
            lines.append(f"- {skill}")
        lines.append("")
    
    # Missing skills
    if missing_skills:
        lines.append("### ✗ Missing Skills")
        for skill_info in missing_skills:
            skill_name = skill_info.get('skill_name', 'Unknown')
            importance = skill_info.get('importance', 'preferred')
            importance_emoji = {
                'critical': '🔴',
                'preferred': '🟡',
                'nice-to-have': '🟢'
            }.get(importance, '⚪')
            lines.append(f"- {skill_name} ({importance}) {importance_emoji}")
        lines.append("")
    
    # Recommendation
    lines.append("### Recommendation")
    if recommendation == 'strong-match':
        lines.append("This candidate is a **strong match** for the position. "
                    "They possess most of the required skills and their background "
                    "aligns well with the job requirements.")
    elif recommendation == 'good-match':
        lines.append("This candidate is a **good match** for the position. "
                    "They have many relevant skills, though there may be some gaps "
                    "that could be addressed through training.")
    elif recommendation == 'weak-match':
        lines.append("This candidate is a **weak match** for the position. "
                    "There are significant skill gaps that would need to be addressed. "
                    "Consider if the candidate has transferable skills or potential for growth.")
    else:
        lines.append("This candidate is **not a match** for the position based on the "
                    "current requirements. Consider other candidates or review if "
                    "requirements can be adjusted.")
    
    return "\n".join(lines)


def generate_skill_gap_analysis(
    resume_skills: List[str],
    required_skills: List[Dict]
) -> Dict[str, Any]:
    """
    Generate a detailed skill gap analysis.
    
    Args:
        resume_skills: Skills from resume
        required_skills: Required skills with importance
        
    Returns:
        Skill gap analysis dictionary
    """
    resume_skills_lower = {s.lower(): s for s in resume_skills}
    
    analysis = {
        'critical_matched': [],
        'critical_missing': [],
        'preferred_matched': [],
        'preferred_missing': [],
        'nice_to_have_matched': [],
        'nice_to_have_missing': [],
        'extra_skills': []
    }
    
    required_skills_lower = set()
    
    for req in required_skills:
        skill_name = req.get('skill_name', '')
        importance = req.get('importance', 'preferred')
        required_skills_lower.add(skill_name.lower())
        
        if skill_name.lower() in resume_skills_lower:
            if importance == 'critical':
                analysis['critical_matched'].append(skill_name)
            elif importance == 'preferred':
                analysis['preferred_matched'].append(skill_name)
            else:
                analysis['nice_to_have_matched'].append(skill_name)
        else:
            if importance == 'critical':
                analysis['critical_missing'].append(skill_name)
            elif importance == 'preferred':
                analysis['preferred_missing'].append(skill_name)
            else:
                analysis['nice_to_have_missing'].append(skill_name)
    
    # Find extra skills not in requirements
    for skill_lower, skill_original in resume_skills_lower.items():
        if skill_lower not in required_skills_lower:
            analysis['extra_skills'].append(skill_original)
    
    return analysis


def format_skill_gap_report(analysis: Dict[str, Any]) -> str:
    """
    Format skill gap analysis as a readable report.
    
    Args:
        analysis: Skill gap analysis dictionary
        
    Returns:
        Formatted report string
    """
    lines = ["## Skill Gap Analysis\n"]
    
    # Critical skills
    lines.append("### Critical Skills")
    if analysis['critical_matched']:
        lines.append("**✓ Matched:**")
        for skill in analysis['critical_matched']:
            lines.append(f"  - {skill}")
    if analysis['critical_missing']:
        lines.append("**✗ Missing:**")
        for skill in analysis['critical_missing']:
            lines.append(f"  - {skill}")
    if not analysis['critical_matched'] and not analysis['critical_missing']:
        lines.append("No critical skills specified.")
    lines.append("")
    
    # Preferred skills
    lines.append("### Preferred Skills")
    if analysis['preferred_matched']:
        lines.append("**✓ Matched:**")
        for skill in analysis['preferred_matched']:
            lines.append(f"  - {skill}")
    if analysis['preferred_missing']:
        lines.append("**✗ Missing:**")
        for skill in analysis['preferred_missing']:
            lines.append(f"  - {skill}")
    lines.append("")
    
    # Nice-to-have skills  
    lines.append("### Nice-to-Have Skills")
    if analysis['nice_to_have_matched']:
        lines.append("**✓ Matched:**")
        for skill in analysis['nice_to_have_matched']:
            lines.append(f"  - {skill}")
    if analysis['nice_to_have_missing']:
        lines.append("**✗ Missing:**")
        for skill in analysis['nice_to_have_missing']:
            lines.append(f"  - {skill}")
    lines.append("")
    
    # Extra skills
    if analysis['extra_skills']:
        lines.append("### Additional Skills (Not Required)")
        for skill in analysis['extra_skills']:
            lines.append(f"  - {skill}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Test explanation
    sample_result = {
        'overall_score': 0.72,
        'recommendation': 'good-match',
        'subscores': {
            'skill_match': 0.65,
            'semantic_similarity': 0.79
        },
        'matched_skills': ['Python', 'React', 'Machine Learning'],
        'missing_skills': [
            {'skill_name': 'AWS', 'importance': 'critical'},
            {'skill_name': 'Docker', 'importance': 'preferred'}
        ]
    }
    
    explanation = generate_match_explanation(sample_result)
    print(explanation)
