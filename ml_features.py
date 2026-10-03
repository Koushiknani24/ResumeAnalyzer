"""Lightweight deterministic text comparison utilities."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_tfidf_similarity(resume_text: str, job_description: str) -> float:
    """Return lexical similarity for two non-empty texts; this is not an ATS score."""
    if not resume_text.strip() or not job_description.strip():
        return 0.0
    try:
        matrix = TfidfVectorizer(stop_words="english").fit_transform([resume_text, job_description])
        return round(float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0]) * 100, 2)
    except ValueError:
        return 0.0
