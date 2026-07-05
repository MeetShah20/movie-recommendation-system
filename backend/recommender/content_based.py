"""Content-based recommendations from the movie metadata soup."""

from sklearn.feature_extraction.text import TfidfVectorizer


def fit_tfidf(soup):
    """Fit a TF-IDF vectorizer on the metadata soup and return it with the matrix."""
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(soup)
    return vectorizer, matrix
