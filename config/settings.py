"""
AI Resume Screener - Configuration Settings
Contains all paths, thresholds, and model parameters.
Reads from environment variables with safe defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Data subdirectories
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DATASETS_DIR = DATA_DIR / "datasets"

# Model subdirectories
SAVED_MODELS_DIR = MODELS_DIR / "saved"
PRETRAINED_DIR = MODELS_DIR / "pretrained"

# Skills taxonomy path
SKILLS_TAXONOMY_PATH = DATASETS_DIR / "skills_taxonomy.json"

# PDF Processing Constraints
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_RESUME_PAGES = 10
MAX_EXTRACTED_TEXT_LENGTH = 50000
SUPPORTED_PDF_VERSIONS = ["1.4", "1.5", "1.6", "1.7"]
PROCESSING_TIMEOUT_SECONDS = 60

# Text Processing
TEXT_ENCODING = "utf-8"
MIN_TEXT_LENGTH = 100

# NLP Settings
SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_md")
VECTOR_DIMENSIONALITY = 300
MIN_SKILL_CONFIDENCE = 0.7

# Scoring Weights
SCORING_WEIGHTS = {
    "skill_match": 0.5,
    "semantic_similarity": 0.5
}

# Skill Importance Weights
SKILL_IMPORTANCE_WEIGHTS = {
    "critical": 1.0,
    "preferred": 0.6,
    "nice-to-have": 0.3
}

# Match Thresholds
MATCH_THRESHOLDS = {
    "strong-match": 0.75,
    "good-match": 0.55,
    "weak-match": 0.35,
    "no-match": 0.0
}

# API Settings — read from env for Docker/production overrides
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() in ("true", "1", "yes")

# Streamlit Settings
STREAMLIT_HOST = os.getenv("STREAMLIT_HOST", "localhost")
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

# Memory limits
MIN_RAM_GB = 4
SPACY_MODEL_MEMORY_MB = 200


def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        DATASETS_DIR,
        SAVED_MODELS_DIR,
        PRETRAINED_DIR,
        LOGS_DIR
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_directories()
    print(f"Base directory: {BASE_DIR}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Models directory: {MODELS_DIR}")
