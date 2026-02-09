# System Architecture

## Overview

AI Resume Screener follows a pipeline-based architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interfaces                          │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐               │
│  │ Streamlit │    │  REST API │    │    CLI    │               │
│  │    UI     │    │  (Flask)  │    │           │               │
│  └─────┬─────┘    └─────┬─────┘    └─────┬─────┘               │
└────────┼────────────────┼────────────────┼──────────────────────┘
         │                │                │
         └────────────────┼────────────────┘
                          │
         ┌────────────────▼────────────────┐
         │       Screening Pipeline        │
         │   (Orchestration Layer)         │
         └────────────────┬────────────────┘
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
┌───▼───┐           ┌─────▼─────┐         ┌────▼────┐
│ Pre-  │           │  Feature  │         │Matching │
│process│───────────▶Engineering│─────────▶ Engine  │
│ Module│           │   Module  │         │         │
└───────┘           └───────────┘         └─────────┘
```

## Component Details

### 1. Preprocessing Module
- **pdf_extractor.py**: Extracts raw text from PDF files
- **text_cleaner.py**: Normalizes and cleans extracted text
- **parser.py**: Extracts structured info (name, email, phone)

### 2. Feature Engineering Module
- **skill_extractor.py**: Identifies skills using NLP + taxonomy
- **vectorizer.py**: Creates document embeddings (spaCy)
- **keyword_analyzer.py**: Extracts relevant keywords

### 3. Matching Engine
- **similarity_scorer.py**: Calculates match scores
- **explainer.py**: Generates human-readable explanations

### 4. Data Models
- **Resume**: Candidate data structure
- **JobDescription**: Job posting structure
- **MatchResult**: Scoring output structure

## Data Flow

```
PDF Resume ──▶ Text Extraction ──▶ Text Cleaning ──▶ Skill Extraction
                                                           │
                                                           ▼
Job Description ──▶ Skill Parsing ──▶ Vectorization ◀──────┤
                                            │              │
                                            ▼              ▼
                                    Similarity Calc ◀── Skill Match
                                            │
                                            ▼
                                    Match Result + Explanation
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| NLP | spaCy (en_core_web_md) |
| ML | scikit-learn |
| PDF | pdfplumber, PyPDF2 |
| Web UI | Streamlit |
| API | Flask |
| Config | YAML |
