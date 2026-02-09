# Development Log

## v0.1 Development Notes

### Phase 1: Project Setup
- Established project structure following modular design
- Created configuration management with centralized settings
- Implemented logging infrastructure

### Phase 2: Core Modules
- Built PDF extraction with pdfplumber (primary) and PyPDF2 (fallback)
- Implemented text cleaning and resume parsing
- Created skill extraction using taxonomy matching

### Phase 3: Feature Engineering
- Integrated spaCy for document vectorization
- Implemented keyword analysis utilities
- Created TF-IDF vectorizer (optional)

### Phase 4: Matching Engine
- Implemented weighted scoring algorithm
- Created skill match calculation with importance weights
- Built explanation generator for match results

### Phase 5: User Interfaces
- Built Streamlit web interface
- Created Flask REST API
- Implemented CLI tool

---

## Design Decisions

1. **spaCy over BERT**: Chose spaCy for better performance on consumer hardware
2. **Dual PDF libraries**: pdfplumber for accuracy, PyPDF2 as fallback
3. **Taxonomy-based skills**: More reliable than pure NLP extraction
4. **50/50 scoring**: Balanced skill match and semantic similarity

---

## Known Limitations

- English language only
- Single-job matching (no batch ranking)
- No database persistence in v0.1
