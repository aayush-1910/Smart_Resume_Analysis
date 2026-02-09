"""
Download Pre-trained Models Script
Downloads required spaCy and other models.
"""
import subprocess
import sys


def download_spacy_model():
    """Download spaCy English model."""
    print("Downloading spaCy en_core_web_md model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_md"])
    print("Download complete!")


def verify_model():
    """Verify model is loaded correctly."""
    try:
        import spacy
        nlp = spacy.load("en_core_web_md")
        print(f"Model loaded successfully: {nlp.meta['name']} v{nlp.meta['version']}")
        print(f"Vector size: {nlp.vocab.vectors_length}")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False


if __name__ == "__main__":
    download_spacy_model()
    verify_model()
