# AI Resume Screener v0.1

An end-to-end machine learning system designed to analyze resumes and match candidates to relevant job roles.

## Overview

AI Resume Screener extracts structured information from unstructured resume documents, identifies skills and experience signals using natural language processing, and generates a relevance score against job descriptions.

## Features

- **Modern UI/UX**: Clean, futuristic dark-themed interface with glassmorphism effects
- **Multi-Job Comparison**: Compare a resume against 3-5 job descriptions simultaneously
- **Resume Improvement**: Get actionable feedback on missing keywords, formatting, and content
- **Batch Processing**: Screen up to 10 resumes at once with CSV export
- **Learning Recommendations**: Personalized course suggestions for missing skills
- **PDF Text Extraction** - Extract and clean text from resume PDFs
- **Skill Identification** - NLP-powered skill extraction and categorization
- **Resume-Job Matching** - Semantic similarity and skill-based scoring
- **Interpretable Results** - Clear match scores with skill overlap explanations

## Project Structure

```
ai-resume-screener/
├── config/           # Configuration files
├── data/             # Data storage (raw, processed, datasets)
├── models/           # Saved ML models and pretrained assets
├── src/              # Core source code
├── pipeline/         # Main orchestration pipeline
├── api/              # REST API (Flask/FastAPI)
├── ui/               # Streamlit web interface
├── cli/              # Command-line interface
├── tests/            # Unit and integration tests
├── notebooks/        # Jupyter notebooks for exploration
├── docs/             # Documentation
├── scripts/          # Utility scripts
└── logs/             # Application logs
```

## Quick Start

### Prerequisites

- Python 3.9-3.11 (Recommended: 3.10)
- 4 GB RAM minimum

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-resume-screener
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_md
```

### Usage

**Web Interface (Streamlit):**
```bash
streamlit run ui/streamlit_app.py
```

**Command Line:**
```bash
python cli/main.py --resume path/to/resume.pdf --job "Job description text"
```

**API Server:**
```bash
python api/app.py
```

## Technology Stack

- **Language**: Python 3.10
- **NLP**: spaCy (en_core_web_md)
- **ML**: scikit-learn
- **PDF Processing**: pdfplumber, PyPDF2
- **Web UI**: Streamlit
- **API**: Flask/FastAPI

## Scoring Algorithm

The system uses a weighted scoring approach:
- **Skill Match**: 50% weight
- **Semantic Similarity**: 50% weight

Match recommendations:
- ≥0.75: Strong Match
- ≥0.55: Good Match
- ≥0.35: Weak Match
- <0.35: No Match

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api_reference.md)
- [User Guide](docs/user_guide.md)

## License

MIT License - See [LICENSE](LICENSE) for details.

## Development

See [Development Log](docs/development_log.md) for progress notes.

---

*Built as a portfolio project demonstrating NLP and ML skills in hiring-tech applications.*
