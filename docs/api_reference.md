# API Reference

## REST API Endpoints

### Health Check
```
GET /health
```
Returns system health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1"
}
```

---

### Screen Resume
```
POST /api/screen
```
Screen a resume against a job description.

**Request:**
- `resume` (file): PDF resume file
- `job_description` (form): Job description text
- `job_title` (form, optional): Job title

**Response:**
```json
{
  "resume": {...},
  "job": {...},
  "match": {
    "overall_score": 0.72,
    "recommendation": "good-match",
    "matched_skills": ["Python", "React"],
    "missing_skills": [...]
  }
}
```

---

### Extract Text
```
POST /api/extract
```
Extract text from a PDF file.

**Request:**
- `resume` (file): PDF file

**Response:**
```json
{
  "text": "...",
  "num_pages": 2,
  "extraction_method": "pdfplumber",
  "success": true
}
```

---

### Extract Skills
```
POST /api/skills
```
Extract skills from text.

**Request:**
```json
{
  "text": "Resume or job description text..."
}
```

**Response:**
```json
{
  "skills": [
    {"skill_name": "Python", "category": "technical", "confidence": 0.85}
  ]
}
```

---

## Python API

### ScreeningPipeline

```python
from pipeline import ScreeningPipeline

pipeline = ScreeningPipeline()
result = pipeline.screen_resume(
    pdf_path="resume.pdf",
    job_text="Job description...",
    job_title="Software Engineer"
)
```

### Core Functions

```python
# Text extraction
from src.preprocessing import extract_text_from_pdf
result = extract_text_from_pdf("resume.pdf")

# Skill extraction
from src.feature_engineering import extract_skills
skills = extract_skills("Resume text...")

# Scoring
from src.matching import calculate_match_score
result = calculate_match_score(resume_vec, job_vec, skills, required)
```
