"""
Job Description Data Model
Defines the JobDescription data structure.
"""
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import numpy as np


@dataclass
class JobDescription:
    """Job description data model following the defined schema."""
    
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    company: Optional[str] = None
    description: str = ""
    required_skills: List[Dict[str, str]] = field(default_factory=list)
    min_experience_years: Optional[int] = None
    vector_representation: Optional[np.ndarray] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "job_id": self.job_id,
            "title": self.title[:200] if len(self.title) > 200 else self.title,
            "company": self.company,
            "description": self.description[:10000] if len(self.description) > 10000 else self.description,
            "required_skills": self.required_skills,
            "min_experience_years": self.min_experience_years,
            "vector_representation": self.vector_representation.tolist() if self.vector_representation is not None else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobDescription':
        """Create JobDescription from dictionary."""
        vector = data.get('vector_representation')
        if vector and not isinstance(vector, np.ndarray):
            vector = np.array(vector)
        
        return cls(
            job_id=data.get('job_id', str(uuid.uuid4())),
            title=data.get('title', ''),
            company=data.get('company'),
            description=data.get('description', ''),
            required_skills=data.get('required_skills', []),
            min_experience_years=data.get('min_experience_years'),
            vector_representation=vector
        )
    
    @classmethod
    def from_text(cls, text: str, title: str = "Untitled Job") -> 'JobDescription':
        """Create JobDescription from plain text."""
        return cls(
            title=title,
            description=text
        )
    
    def get_critical_skills(self) -> List[str]:
        """Get list of critical skill names."""
        return [
            s.get('skill_name', '') 
            for s in self.required_skills 
            if s.get('importance') == 'critical'
        ]
    
    def get_all_skill_names(self) -> List[str]:
        """Get all skill names."""
        return [s.get('skill_name', '') for s in self.required_skills]
    
    def add_skill(self, skill_name: str, importance: str = 'preferred') -> None:
        """Add a required skill."""
        self.required_skills.append({
            'skill_name': skill_name,
            'importance': importance
        })
    
    def __repr__(self) -> str:
        return f"JobDescription(id={self.job_id[:8]}..., title={self.title[:30]})"
