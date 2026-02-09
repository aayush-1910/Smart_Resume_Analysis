"""
API Routes Module
Defines API endpoints for the resume screener.
"""
from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/match', methods=['POST'])
def match_resume():
    """Match resume to job description."""
    # Route implementation in app.py
    pass


@api_bp.route('/batch', methods=['POST'])
def batch_screen():
    """Screen multiple resumes against one job."""
    # Not implemented in v0.1
    return jsonify({'error': 'Not implemented in v0.1'}), 501
