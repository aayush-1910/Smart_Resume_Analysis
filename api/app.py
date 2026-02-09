"""
Flask/FastAPI Application
REST API for AI Resume Screener
"""
from flask import Flask, request, jsonify
from pathlib import Path
import tempfile
import os
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'version': '0.1'})


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
    job_description = request.form.get('job_description', '')
    job_title = request.form.get('job_title', 'Job Position')
    
    if not job_description:
        return jsonify({'error': 'No job description provided'}), 400
    
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
        return jsonify({'error': str(e)}), 500
    finally:
        os.unlink(tmp_path)


@app.route('/api/extract', methods=['POST'])
def extract_text():
    """Extract text from a resume PDF."""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    resume_file = request.files['resume']
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        resume_file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        from src.preprocessing import extract_text_from_pdf
        result = extract_text_from_pdf(tmp_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.unlink(tmp_path)


@app.route('/api/skills', methods=['POST'])
def extract_skills():
    """Extract skills from text."""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        from src.feature_engineering import extract_skills as do_extract
        skills = do_extract(text)
        return jsonify({'skills': skills})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    from config.settings import API_HOST, API_PORT, DEBUG_MODE
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG_MODE)
