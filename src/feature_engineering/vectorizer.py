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
    """Get or load spaCy model if available, return None if not."""
    global _nlp
    if _nlp is None:
        if not SPACY_AVAILABLE:
            logger.warning("spaCy not available")
            return None
        try:
            _nlp = spacy.load(SPACY_MODEL)
            logger.info(f"Successfully loaded {SPACY_MODEL}")
        except OSError:
            # Model not found - log warning and return None
            logger.warning(f"spaCy model '{SPACY_MODEL}' not available. Falling back to TF-IDF vectorization.")
            _nlp = False  # Mark as unavailable to avoid repeated attempts
            return None
    return _nlp if _nlp is not False else None


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
    Create document vector using spaCy word embeddings, or fallback to simple TF-IDF.
    
    Args:
        text: Document text
        
    Returns:
        Vector representation, shape (300,)
    """
    nlp = get_spacy_model()
    
    if nlp is None:
        # Fallback: Use simple TF-IDF-like approach with sklearn
        logger.info("Using TF-IDF fallback for vectorization")
        return create_simple_tfidf_vector(text)
    
    doc = nlp(text)
    
    # Get the document vector (average of word vectors)
    vector = doc.vector
    
    if vector.shape[0] != VECTOR_DIMENSIONALITY:
        logger.warning(f"Vector dimension mismatch: {vector.shape[0]} != {VECTOR_DIMENSIONALITY}")
    
    return vector


def create_simple_tfidf_vector(text: str) -> np.ndarray:
    """
    Create a simple TF-IDF-based vector when spaCy is unavailable.
    Uses sklearn's TfidfVectorizer with a fixed vocabulary.
    
    Args:
        text: Document text
        
    Returns:
        Vector of shape (300,) for compatibility
    """
    if not SKLEARN_AVAILABLE:
        logger.error("Neither spaCy nor sklearn available for vectorization")
        return np.zeros(VECTOR_DIMENSIONALITY)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    # Create a simple vectorizer with limited features
    vectorizer = TfidfVectorizer(
        max_features=VECTOR_DIMENSIONALITY,
        stop_words='english',
        ngram_range=(1, 2),
        lowercase=True
    )
    
    # Fit and transform on the single document
    # Note: This is not ideal but works for single-document scenarios
    try:
        vector = vectorizer.fit_transform([text]).toarray()[0]
        
        # Ensure correct dimensionality
        if vector.shape[0] < VECTOR_DIMENSIONALITY:
            # Pad with zeros
            vector = np.pad(vector, (0, VECTOR_DIMENSIONALITY - vector.shape[0]))
        elif vector.shape[0] > VECTOR_DIMENSIONALITY:
            # Truncate
            vector = vector[:VECTOR_DIMENSIONALITY]
            
        return vector
    except Exception as e:
        logger.error(f"Error in TF-IDF vectorization: {e}")
        return np.zeros(VECTOR_DIMENSIONALITY)


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
