"""Content-based recommendations from the movie metadata soup."""

from sklearn.feature_extraction.text import TfidfVectorizer


def fit_tfidf(soup):
    """Fit a TF-IDF vectorizer on the metadata soup and return it with the matrix."""
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(soup)
    return vectorizer, matrix


def build_id_index(movie_ids):
    """Map movie ids to matrix rows and back, following the soup's row order."""
    row_to_id = list(movie_ids)
    id_to_row = {movie_id: row for row, movie_id in enumerate(row_to_id)}
    return id_to_row, row_to_id
