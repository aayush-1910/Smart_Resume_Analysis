#!/bin/bash
# Environment Setup Script

echo "Setting up AI Resume Screener environment..."

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_md

# Create necessary directories
mkdir -p data/raw data/processed data/datasets
mkdir -p models/saved models/pretrained
mkdir -p logs

echo "Setup complete!"
echo "Activate environment: source venv/bin/activate"
echo "Run web UI: streamlit run ui/streamlit_app.py"
