"""Collaborative recommendations from user ratings via latent factors."""

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD


def load_ratings(ratings_path, links_path):
    """Load ratings and translate their MovieLens movieId to the TMDb id used elsewhere.

    ratings_small.csv keys movies by MovieLens movieId, while the rest of the app
    keys by TMDb id. links.csv bridges the two. Ratings whose movie has no TMDb id
    are dropped.
    """
    ratings = pd.read_csv(ratings_path)
    links = pd.read_csv(links_path)[["movieId", "tmdbId"]].dropna(subset=["tmdbId"])
    links["tmdbId"] = links["tmdbId"].astype(int)
    ratings = ratings.merge(links, on="movieId", how="inner")
    return ratings[["userId", "tmdbId", "rating"]].rename(columns={"tmdbId": "movie_id"})


def build_index(values):
    """Map a set of ids to contiguous matrix positions and back."""
    unique = sorted(set(values))
    to_pos = {value: pos for pos, value in enumerate(unique)}
    return to_pos, unique


def build_matrix(ratings, user_to_row, movie_to_col):
    """Build a sparse user-item rating matrix from the translated ratings."""
    rows = ratings["userId"].map(user_to_row)
    cols = ratings["movie_id"].map(movie_to_col)
    shape = (len(user_to_row), len(movie_to_col))
    return csr_matrix((ratings["rating"], (rows, cols)), shape=shape)


def fit_svd(matrix, n_components=50):
    """Factorize the ratings matrix into latent user and movie factors."""
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    user_factors = svd.fit_transform(matrix)
    movie_factors = svd.components_.T
    return user_factors, movie_factors
