"""
Flask REST API for AI Resume Screener
Production-hardened with error handling, CORS, file validation, and health checks.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import tempfile
import os
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__)

# Enable CORS for cross-origin requests (deployed frontends)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Limit upload size (5 MB default, matches MAX_FILE_SIZE_MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


# ---- Global Error Handlers --------------------------------------------------

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad request', 'detail': str(e)}), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(413)
def request_entity_too_large(e):
    return jsonify({'error': 'File too large', 'detail': 'Maximum upload size is 5 MB'}), 413


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error', 'detail': str(e)}), 500


# ---- Utility ---------------------------------------------------------------

def validate_pdf_file(file_storage):
    """Validate that an uploaded file is actually a PDF.
    
    Args:
        file_storage: Flask FileStorage object
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_storage or not file_storage.filename:
        return False, "No file provided"
    
    # Check extension
    if not file_storage.filename.lower().endswith('.pdf'):
        return False, "File must be a PDF"
    
    # Check magic bytes (%PDF)
    header = file_storage.read(5)
    file_storage.seek(0)  # Reset position
    
    if not header.startswith(b'%PDF'):
        return False, "File is not a valid PDF (invalid header)"
    
    return True, None


# ---- Endpoints --------------------------------------------------------------

@app.route('/health', methods=['GET'])
def health():
    """Health check with dependency status."""
    status = {
        'status': 'healthy',
        'version': '0.2.0',
        'dependencies': {}
    }
    
    # Check spaCy model
    try:
        from src.feature_engineering.vectorizer import get_spacy_model
        nlp = get_spacy_model()
        status['dependencies']['spacy_model'] = 'loaded' if nlp else 'unavailable (using TF-IDF fallback)'
    except Exception:
        status['dependencies']['spacy_model'] = 'error'
    
    # Check skills taxonomy
    try:
        from config.settings import SKILLS_TAXONOMY_PATH
        status['dependencies']['skills_taxonomy'] = 'loaded' if SKILLS_TAXONOMY_PATH.exists() else 'missing'
    except Exception:
        status['dependencies']['skills_taxonomy'] = 'error'
    
    # Check skill synonyms
    try:
        from src.feature_engineering.skill_extractor import SKILL_SYNONYMS_PATH
        status['dependencies']['skill_synonyms'] = 'loaded' if SKILL_SYNONYMS_PATH.exists() else 'missing'
    except Exception:
        status['dependencies']['skill_synonyms'] = 'error'
    
    return jsonify(status)


@app.route('/api/screen', methods=['POST'])
def screen_resume():
    """
    Screen a resume against a job description.
    
    Expects:
        - resume: PDF file
        - job_description: str
        - job_title: str (optional)
    """
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    resume_file = request.files['resume']
    
    # Validate PDF
    is_valid, error_msg = validate_pdf_file(resume_file)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    job_description = request.form.get('job_description', '')
    job_title = request.form.get('job_title', 'Job Position')
    
    if not job_description or len(job_description.strip()) < 20:
        return jsonify({'error': 'Job description is too short (minimum 20 characters)'}), 400
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        resume_file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        from pipeline.screening_pipeline import ScreeningPipeline
        
        pipeline = ScreeningPipeline()
        result = pipeline.screen_resume(tmp_path, job_description, job_title)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Screening failed: {str(e)}'}), 500
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.route('/api/extract', methods=['POST'])
def extract_text():
    """Extract text from a resume PDF."""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    resume_file = request.files['resume']
    
    # Validate PDF
    is_valid, error_msg = validate_pdf_file(resume_file)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        resume_file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        from src.preprocessing import extract_text_from_pdf
        result = extract_text_from_pdf(tmp_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Text extraction failed: {str(e)}'}), 500
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.route('/api/skills', methods=['POST'])
def extract_skills():
    """Extract skills from text."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    text = data.get('text', '')
    
    if not text or len(text.strip()) < 20:
        return jsonify({'error': 'Text is too short (minimum 20 characters)'}), 400
    
    try:
        from src.feature_engineering import extract_skills as do_extract
        skills = do_extract(text)
        return jsonify({'skills': skills})
    except Exception as e:
        return jsonify({'error': f'Skill extraction failed: {str(e)}'}), 500


if __name__ == '__main__':
    from config.settings import API_HOST, API_PORT, DEBUG_MODE
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG_MODE)
