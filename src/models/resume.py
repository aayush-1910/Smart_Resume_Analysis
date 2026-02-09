"""
Resume Data Model
Defines the Resume data structure.
"""
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import numpy as np


@dataclass
class Resume:
    """Resume data model following the defined schema."""
    
    resume_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Candidate info
    name: str = "Unknown"
    email: Optional[str] = None
    phone: Optional[str] = None
    
    # Content
    extracted_text: str = ""
    skills: List[Dict[str, Any]] = field(default_factory=list)
    experience_years: Optional[int] = None
    education_level: Optional[str] = None
    
    # Vector representation
    vector_representation: Optional[np.ndarray] = None
    
    # Processing metadata
    extraction_method: str = ""
    num_pages: int = 0
    file_size_bytes: int = 0
    source_file: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "resume_id": self.resume_id,
            "timestamp": self.timestamp,
            "candidate": {
                "name": self.name,
                "email": self.email,
                "phone": self.phone
            },
            "extracted_text": self.extracted_text[:1000] + "..." if len(self.extracted_text) > 1000 else self.extracted_text,
            "skills": self.skills,
            "experience_years": self.experience_years,
            "education_level": self.education_level,
            "vector_representation": self.vector_representation.tolist() if self.vector_representation is not None else None,
            "processing_metadata": {
                "extraction_method": self.extraction_method,
                "num_pages": self.num_pages,
                "file_size_bytes": self.file_size_bytes
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Resume':
        """Create Resume from dictionary."""
        candidate = data.get('candidate', {})
        metadata = data.get('processing_metadata', {})
        
        vector = data.get('vector_representation')
        if vector and not isinstance(vector, np.ndarray):
            vector = np.array(vector)
        
        return cls(
            resume_id=data.get('resume_id', str(uuid.uuid4())),
            timestamp=data.get('timestamp', datetime.utcnow().isoformat()),
            name=candidate.get('name', 'Unknown'),
            email=candidate.get('email'),
            phone=candidate.get('phone'),
            extracted_text=data.get('extracted_text', ''),
            skills=data.get('skills', []),
            experience_years=data.get('experience_years'),
            education_level=data.get('education_level'),
            vector_representation=vector,
            extraction_method=metadata.get('extraction_method', ''),
            num_pages=metadata.get('num_pages', 0),
            file_size_bytes=metadata.get('file_size_bytes', 0)
        )
    
    def get_skill_names(self) -> List[str]:
        """Get list of skill names."""
        return [s.get('skill_name', '') for s in self.skills]
    
    def get_skills_by_category(self, category: str) -> List[Dict]:
        """Get skills filtered by category."""
        return [s for s in self.skills if s.get('category') == category]
    
    def __repr__(self) -> str:
        return f"Resume(id={self.resume_id[:8]}..., name={self.name}, skills={len(self.skills)})"
