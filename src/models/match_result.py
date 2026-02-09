"""
Match Result Data Model
Defines the MatchResult data structure.
"""
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class MatchResult:
    """Match result data model following the defined schema."""
    
    match_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resume_id: Optional[str] = None
    job_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    overall_score: float = 0.0
    skill_match_score: float = 0.0
    experience_match_score: float = 0.0
    semantic_similarity_score: float = 0.0
    
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[Dict[str, str]] = field(default_factory=list)
    recommendation: str = "no-match"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "match_id": self.match_id,
            "resume_id": self.resume_id,
            "job_id": self.job_id,
            "timestamp": self.timestamp,
            "overall_score": round(self.overall_score, 3),
            "subscores": {
                "skill_match": round(self.skill_match_score, 3),
                "experience_match": round(self.experience_match_score, 3),
                "semantic_similarity": round(self.semantic_similarity_score, 3)
            },
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills,
            "recommendation": self.recommendation
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MatchResult':
        """Create MatchResult from dictionary."""
        subscores = data.get('subscores', {})
        
        return cls(
            match_id=data.get('match_id', str(uuid.uuid4())),
            resume_id=data.get('resume_id'),
            job_id=data.get('job_id'),
            timestamp=data.get('timestamp', datetime.utcnow().isoformat()),
            overall_score=data.get('overall_score', 0.0),
            skill_match_score=subscores.get('skill_match', 0.0),
            experience_match_score=subscores.get('experience_match', 0.0),
            semantic_similarity_score=subscores.get('semantic_similarity', 0.0),
            matched_skills=data.get('matched_skills', []),
            missing_skills=data.get('missing_skills', []),
            recommendation=data.get('recommendation', 'no-match')
        )
    
    def is_strong_match(self) -> bool:
        """Check if this is a strong match."""
        return self.recommendation == 'strong-match'
    
    def is_acceptable(self) -> bool:
        """Check if match is at least acceptable (good or strong)."""
        return self.recommendation in ['strong-match', 'good-match']
    
    def get_recommendation_emoji(self) -> str:
        """Get emoji for recommendation level."""
        emojis = {
            'strong-match': '🟢',
            'good-match': '🟡',
            'weak-match': '🟠',
            'no-match': '🔴'
        }
        return emojis.get(self.recommendation, '⚪')
    
    def __repr__(self) -> str:
        return f"MatchResult(score={self.overall_score:.2f}, rec={self.recommendation})"
