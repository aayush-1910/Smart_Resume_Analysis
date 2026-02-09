# User Guide

## Quick Start

### Web Interface (Recommended)
```bash
streamlit run ui/streamlit_app.py
```
Then open http://localhost:8501 in your browser.

### Command Line
```bash
python cli/main.py screen --resume resume.pdf --job "Job description..."
```

---

## Using the Web Interface

1. **Upload Resume**: Click "Browse files" or drag-and-drop a PDF resume
2. **Enter Job Details**: Type the job title and paste the job description
3. **Click Analyze**: Press the "Analyze Match" button
4. **View Results**: See match score, matched/missing skills, and recommendations

---

## Using the CLI

### Screen a Resume
```bash
python cli/main.py screen \
  --resume path/to/resume.pdf \
  --job "We are looking for a Python developer..." \
  --title "Software Engineer"
```

### Extract Text from PDF
```bash
python cli/main.py extract --file resume.pdf
```

### Extract Skills from Text
```bash
python cli/main.py skills --text "Python developer with React experience"
```

---

## Understanding Match Scores

| Score | Recommendation | Meaning |
|-------|----------------|---------|
| ≥75% | Strong Match | Excellent fit, most skills matched |
| 55-74% | Good Match | Good fit, some gaps |
| 35-54% | Weak Match | Partial fit, significant gaps |
| <35% | No Match | Poor fit for this role |

---

## Supported File Formats

- **Resume**: PDF only (max 5MB, 10 pages)
- **Job Description**: Plain text

---

## Troubleshooting

**"spaCy model not found"**
```bash
python -m spacy download en_core_web_md
```

**"PDF extraction failed"**
- Ensure PDF is not password-protected
- Check if PDF contains actual text (not scanned images)
