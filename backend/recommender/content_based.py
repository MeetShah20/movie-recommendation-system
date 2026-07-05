"""Content-based recommendations from the movie metadata soup."""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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


def similar_movies(movie_id, matrix, id_to_row, row_to_id, top_n=10):
    """Return the top_n movies most similar to movie_id by cosine similarity.

    Similarity is computed against the whole matrix on demand. Storing a full
    45k x 45k similarity matrix would take far too much memory, and a single
    query row against the matrix is fast enough to do per request.
    """
    if movie_id not in id_to_row:
        raise KeyError(movie_id)
    row = id_to_row[movie_id]
    scores = cosine_similarity(matrix[row], matrix).ravel()
    ranked = np.argsort(scores)[::-1]
    results = []
    for index in ranked:
        if index == row:
            continue
        results.append((int(row_to_id[index]), float(scores[index])))
        if len(results) == top_n:
            break
    return results
