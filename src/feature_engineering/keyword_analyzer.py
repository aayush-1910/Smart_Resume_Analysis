"""
Keyword Analyzer Module
Extracts and analyzes keywords from text.
"""
import re
from typing import List, Dict, Tuple
from collections import Counter

from config.logging_config import get_logger

logger = get_logger("keyword_analyzer")

# Common stop words to filter out
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
    'they', 'what', 'which', 'who', 'whom', 'when', 'where', 'why', 'how',
    'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'
}


def extract_keywords(
    text: str,
    max_keywords: int = 20,
    min_length: int = 3,
    include_phrases: bool = True
) -> List[Dict]:
    """
    Extract important keywords from text.
    
    Args:
        text: Input text
        max_keywords: Maximum number of keywords to return
        min_length: Minimum keyword length
        include_phrases: Whether to include multi-word phrases
        
    Returns:
        List of keyword dictionaries with 'keyword' and 'count'
    """
    if not text:
        return []
    
    keywords = []
    
    # Extract single words
    words = extract_single_keywords(text, min_length)
    keywords.extend(words)
    
    # Extract phrases
    if include_phrases:
        phrases = extract_key_phrases(text, min_length)
        keywords.extend(phrases)
    
    # Sort by count and return top N
    keywords.sort(key=lambda x: x['count'], reverse=True)
    return keywords[:max_keywords]


def extract_single_keywords(text: str, min_length: int = 3) -> List[Dict]:
    """
    Extract single-word keywords.
    
    Args:
        text: Input text
        min_length: Minimum word length
        
    Returns:
        List of keyword dictionaries
    """
    # Tokenize and clean
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter
    filtered = [
        word for word in words
        if len(word) >= min_length and word not in STOP_WORDS
    ]
    
    # Count occurrences
    word_counts = Counter(filtered)
    
    return [
        {'keyword': word, 'count': count, 'type': 'word'}
        for word, count in word_counts.items()
        if count >= 1
    ]


def extract_key_phrases(text: str, min_length: int = 3) -> List[Dict]:
    """
    Extract multi-word key phrases.
    
    Args:
        text: Input text
        min_length: Minimum phrase length
        
    Returns:
        List of phrase dictionaries
    """
    phrases = []
    
    # Common technical phrase patterns
    # Pattern: Adjective + Noun, Noun + Noun
    pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
    matches = re.findall(pattern, text)
    
    # Also look for specific patterns
    tech_patterns = [
        r'\b(\w+\s+(?:development|engineering|management|analysis|design))\b',
        r'\b((?:software|web|mobile|cloud|data)\s+\w+)\b',
        r'\b(\w+\s+(?:learning|processing|science))\b',
    ]
    
    for pattern in tech_patterns:
        matches.extend(re.findall(pattern, text, re.IGNORECASE))
    
    # Clean and count
    phrase_counts = Counter(phrase.lower() for phrase in matches)
    
    for phrase, count in phrase_counts.items():
        if len(phrase) >= min_length and count >= 1:
            phrases.append({
                'keyword': phrase,
                'count': count,
                'type': 'phrase'
            })
    
    return phrases


def compare_keyword_overlap(
    text1_keywords: List[str],
    text2_keywords: List[str]
) -> Tuple[List[str], float]:
    """
    Compare keyword overlap between two texts.
    
    Args:
        text1_keywords: Keywords from first text
        text2_keywords: Keywords from second text
        
    Returns:
        Tuple of (overlapping keywords, overlap ratio)
    """
    set1 = set(k.lower() for k in text1_keywords)
    set2 = set(k.lower() for k in text2_keywords)
    
    overlap = set1 & set2
    
    # Calculate Jaccard similarity
    union = set1 | set2
    ratio = len(overlap) / len(union) if union else 0.0
    
    return list(overlap), ratio


def find_keyword_context(text: str, keyword: str, window: int = 50) -> List[str]:
    """
    Find context around keyword occurrences.
    
    Args:
        text: Full text
        keyword: Keyword to find
        window: Characters before/after to include
        
    Returns:
        List of context strings
    """
    contexts = []
    keyword_lower = keyword.lower()
    text_lower = text.lower()
    
    start = 0
    while True:
        pos = text_lower.find(keyword_lower, start)
        if pos == -1:
            break
        
        context_start = max(0, pos - window)
        context_end = min(len(text), pos + len(keyword) + window)
        context = text[context_start:context_end].strip()
        
        # Add ellipsis if truncated
        if context_start > 0:
            context = "..." + context
        if context_end < len(text):
            context = context + "..."
        
        contexts.append(context)
        start = pos + 1
    
    return contexts


if __name__ == "__main__":
    # Test keyword extraction
    sample = """
    Software Engineer with expertise in Python and Machine Learning.
    Experience in web development using Django and React.
    Strong problem solving and communication skills.
    Background in data science and cloud computing with AWS.
    """
    
    keywords = extract_keywords(sample)
    print("Keywords:")
    for kw in keywords[:10]:
        print(f"  {kw['keyword']} ({kw['type']}): {kw['count']}")
