"""
Skill Extractor Module
Identifies and extracts skills from resume text using NLP.
"""
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import SPACY_MODEL, MIN_SKILL_CONFIDENCE, SKILLS_TAXONOMY_PATH
from config.logging_config import get_logger

logger = get_logger("skill_extractor")

# Global spaCy model reference
_nlp = None


def load_spacy_model():
    """Load spaCy model if available, return None if not."""
    global _nlp
    if _nlp is None:
        if not SPACY_AVAILABLE:
            logger.warning("spaCy not installed")
            return None
        try:
            _nlp = spacy.load(SPACY_MODEL)
            logger.info(f"Loaded spaCy model: {SPACY_MODEL}")
        except OSError:
            # Model not found - skill extraction will work without NLP features
            logger.warning(f"spaCy model '{SPACY_MODEL}' not available. NLP-based skill extraction disabled.")
            _nlp = False  # Mark as unavailable
            return None
    return _nlp if _nlp is not False else None


def load_skills_taxonomy() -> Dict[str, List[str]]:
    """Load skills taxonomy from JSON file."""
    if SKILLS_TAXONOMY_PATH.exists():
        with open(SKILLS_TAXONOMY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Default minimal taxonomy
    return {
        "technical": [
            "Python", "JavaScript", "Java", "C++", "C#", "SQL", "HTML", "CSS",
            "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI",
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
            "TensorFlow", "PyTorch", "Keras", "scikit-learn", "pandas", "numpy",
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "Linux",
            "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",
            "REST API", "GraphQL", "Microservices", "CI/CD", "Agile", "Scrum"
        ],
        "soft": [
            "Communication", "Leadership", "Teamwork", "Problem Solving",
            "Critical Thinking", "Time Management", "Adaptability", "Creativity",
            "Collaboration", "Presentation", "Negotiation", "Mentoring",
            "Project Management", "Decision Making", "Conflict Resolution"
        ],
        "domain": [
            "Finance", "Healthcare", "E-commerce", "Banking", "Insurance",
            "Retail", "Manufacturing", "Logistics", "Education", "Marketing",
            "Sales", "HR", "Legal", "Real Estate", "Consulting"
        ]
    }


def extract_skills(
    text: str,
    skill_taxonomy: Optional[Dict] = None,
    min_confidence: float = MIN_SKILL_CONFIDENCE
) -> List[Dict[str, Any]]:
    """
    Extract skills from text using NLP and taxonomy matching.
    
    Args:
        text: Resume or job description text
        skill_taxonomy: Dictionary with skill categories
        min_confidence: Minimum confidence threshold (0.0-1.0)
        
    Returns:
        List of dictionaries containing:
            - skill_name: Name of the skill
            - category: 'technical', 'soft', or 'domain'
            - confidence: Confidence score (0.0-1.0)
    """
    if not text or len(text.strip()) < 100:
        logger.warning("TEXT_TOO_SHORT: Text has fewer than 100 characters")
        return []
    
    if skill_taxonomy is None:
        skill_taxonomy = load_skills_taxonomy()
    
    extracted_skills = []
    text_lower = text.lower()
    
    # Match skills from taxonomy
    for category, skills in skill_taxonomy.items():
        for skill in skills:
            skill_lower = skill.lower()
            
            # Check for exact match or as word boundary
            patterns = [
                rf'\b{re.escape(skill_lower)}\b',  # Exact word match
                rf'\b{re.escape(skill_lower)}s?\b',  # With optional 's'
            ]
            
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    # Calculate confidence based on match quality
                    confidence = calculate_skill_confidence(skill, text)
                    
                    if confidence >= min_confidence:
                        extracted_skills.append({
                            "skill_name": skill,
                            "category": category,
                            "confidence": round(confidence, 2)
                        })
                    break
    
    # Deduplicate, keeping highest confidence
    skill_map = {}
    for skill in extracted_skills:
        name = skill["skill_name"]
        if name not in skill_map or skill["confidence"] > skill_map[name]["confidence"]:
            skill_map[name] = skill
    
    return list(skill_map.values())


def calculate_skill_confidence(skill: str, text: str) -> float:
    """
    Calculate confidence score for a skill match.
    
    Args:
        skill: Skill name
        text: Full text
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    skill_lower = skill.lower()
    text_lower = text.lower()
    
    # Base confidence
    confidence = 0.7
    
    # Boost for multiple mentions
    count = len(re.findall(rf'\b{re.escape(skill_lower)}\b', text_lower))
    if count > 1:
        confidence += min(0.1 * (count - 1), 0.2)  # Max +0.2 for 3+ mentions
    
    # Boost for appearing near skill-related context
    skill_contexts = ['experience', 'proficient', 'expert', 'skilled', 'knowledge']
    for context in skill_contexts:
        # Check if skill appears near context words
        pattern = rf'{context}.*\b{re.escape(skill_lower)}\b|\b{re.escape(skill_lower)}\b.*{context}'
        if re.search(pattern, text_lower):
            confidence += 0.1
            break
    
    return min(confidence, 1.0)


def extract_skills_with_nlp(text: str) -> List[Dict[str, Any]]:
    """
    Extract skills using spaCy NLP (entity recognition and noun phrases).
    This complements taxonomy-based extraction.
    
    Args:
        text: Resume text
        
    Returns:
        List of potential skill candidates (empty if spaCy unavailable)
    """
    nlp = load_spacy_model()
    
    if nlp is None:
        logger.info("spaCy model not available, skipping NLP-based skill extraction")
        return []
    
    doc = nlp(text)
    
    candidates = []
    
    # Extract noun phrases as potential skills
    for chunk in doc.noun_chunks:
        if 2 <= len(chunk.text) <= 50:
            candidates.append({
                "text": chunk.text,
                "type": "noun_phrase"
            })
    
    # Extract named entities that might be skills/technologies
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'WORK_OF_ART']:
            candidates.append({
                "text": ent.text,
                "type": "entity",
                "label": ent.label_
            })
    
    return candidates


if __name__ == "__main__":
    # Test skill extraction
    sample = """
    Senior Software Engineer with 5+ years of experience in Python and JavaScript.
    Proficient in React, Node.js, and Django. Strong problem solving and communication skills.
    Experience with AWS, Docker, and machine learning using TensorFlow and scikit-learn.
    Background in finance and e-commerce domains.
    """
    
    skills = extract_skills(sample)
    print("Extracted skills:")
    for skill in sorted(skills, key=lambda x: (-x['confidence'], x['skill_name'])):
        print(f"  {skill['skill_name']} ({skill['category']}): {skill['confidence']}")
