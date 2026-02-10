# ============================================================
# AI Resume Screener — Production Dockerfile
# Multi-purpose: runs Streamlit UI (default) or Flask API
# ============================================================
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System dependencies required by pdfplumber / spaCy
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --------------- Dependency layer (cached) -------------------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_md

# --------------- Application layer ---------------------------
COPY . .

# Create required directories
RUN mkdir -p logs data/raw data/processed models/saved models/pretrained

# Expose ports: Streamlit (8501) and Flask API (5000)
EXPOSE 8501 5000

# Health check — Streamlit healthz endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default: run Streamlit UI
CMD ["streamlit", "run", "ui/streamlit_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
