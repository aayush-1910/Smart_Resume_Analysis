"""
Vectorizer Module
Generates TF-IDF or embedding-based vector representations.
"""
import numpy as np
from typing import List, Optional, Union
from pathlib import Path

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import SPACY_MODEL, VECTOR_DIMENSIONALITY
from config.logging_config import get_logger

logger = get_logger("vectorizer")

# Global model reference
_nlp = None


def get_spacy_model():
    """Get or load spaCy model, downloading if necessary."""
    global _nlp
    if _nlp is None:
        if not SPACY_AVAILABLE:
            raise RuntimeError("spaCy not available")
        try:
            _nlp = spacy.load(SPACY_MODEL)
        except OSError:
            # Model not found, download it
            logger.info(f"Downloading spaCy model: {SPACY_MODEL}")
            import subprocess
            subprocess.check_call([
                "python", "-m", "spacy", "download", SPACY_MODEL, "--quiet"
            ])
            _nlp = spacy.load(SPACY_MODEL)
            logger.info(f"Successfully loaded {SPACY_MODEL}")
    return _nlp


def create_document_vector(
    text: str,
    method: str = 'spacy'
) -> np.ndarray:
    """
    Create a vector representation of a document.
    
    Args:
        text: Document text
        method: Vectorization method ('spacy' or 'tfidf')
        
    Returns:
        NumPy array of shape (VECTOR_DIMENSIONALITY,)
    """
    if not text or not text.strip():
        return np.zeros(VECTOR_DIMENSIONALITY)
    
    if method == 'spacy':
        return create_spacy_vector(text)
    elif method == 'tfidf':
        raise NotImplementedError("TF-IDF vectorization requires fitting on corpus")
    else:
        raise ValueError(f"Unknown vectorization method: {method}")


def create_spacy_vector(text: str) -> np.ndarray:
    """
    Create document vector using spaCy word embeddings.
    
    Args:
        text: Document text
        
    Returns:
        Mean of word vectors, shape (300,)
    """
    nlp = get_spacy_model()
    doc = nlp(text)
    
    # Get the document vector (average of word vectors)
    vector = doc.vector
    
    if vector.shape[0] != VECTOR_DIMENSIONALITY:
        logger.warning(f"Vector dimension mismatch: {vector.shape[0]} != {VECTOR_DIMENSIONALITY}")
    
    return vector


def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score between 0.0 and 1.0
    """
    if vec1 is None or vec2 is None:
        return 0.0
    
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    similarity = np.dot(vec1, vec2) / (norm1 * norm2)
    
    # Clamp to [0, 1] (sometimes floating point gives slightly negative values)
    return max(0.0, min(1.0, float(similarity)))


class TfidfDocumentVectorizer:
    """TF-IDF based document vectorizer."""
    
    def __init__(self, max_features: int = 1000):
        """
        Initialize TF-IDF vectorizer.
        
        Args:
            max_features: Maximum number of features
        """
        if not SKLEARN_AVAILABLE:
            raise RuntimeError("scikit-learn not available")
        
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.is_fitted = False
    
    def fit(self, documents: List[str]) -> 'TfidfDocumentVectorizer':
        """
        Fit vectorizer on corpus.
        
        Args:
            documents: List of document texts
            
        Returns:
            Self for chaining
        """
        self.vectorizer.fit(documents)
        self.is_fitted = True
        return self
    
    def transform(self, text: str) -> np.ndarray:
        """
        Transform text to TF-IDF vector.
        
        Args:
            text: Document text
            
        Returns:
            TF-IDF vector
        """
        if not self.is_fitted:
            raise RuntimeError("Vectorizer not fitted. Call fit() first.")
        
        return self.vectorizer.transform([text]).toarray()[0]
    
    def fit_transform(self, documents: List[str]) -> np.ndarray:
        """
        Fit and transform in one step.
        
        Args:
            documents: List of document texts
            
        Returns:
            Matrix of TF-IDF vectors
        """
        self.is_fitted = True
        return self.vectorizer.fit_transform(documents).toarray()


if __name__ == "__main__":
    # Test vectorization
    sample1 = "Python developer with experience in machine learning and data science."
    sample2 = "Software engineer skilled in Python, TensorFlow, and deep learning."
    sample3 = "Marketing manager with excellent communication skills."
    
    print("Testing spaCy vectors...")
    vec1 = create_document_vector(sample1)
    vec2 = create_document_vector(sample2)
    vec3 = create_document_vector(sample3)
    
    print(f"Vector shape: {vec1.shape}")
    print(f"Similarity (1-2): {calculate_cosine_similarity(vec1, vec2):.3f}")
    print(f"Similarity (1-3): {calculate_cosine_similarity(vec1, vec3):.3f}")
    print(f"Similarity (2-3): {calculate_cosine_similarity(vec2, vec3):.3f}")
