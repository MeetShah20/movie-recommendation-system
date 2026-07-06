"""Build the recommender artifacts once, ready to be written to disk."""

from pathlib import Path

from recommender.loading import build_movies
from recommender.features import build_metadata_soup
from recommender.content_based import fit_tfidf, build_id_index
from recommender.collaborative import load_ratings, build_index, build_matrix, fit_svd

BACKEND_DIR = Path(__file__).resolve().parent
DATA_DIR = BACKEND_DIR / "data"
ARTIFACTS_DIR = BACKEND_DIR / "precomputed"


def build(data_dir=DATA_DIR):
    """Load the data and fit both recommenders, returning the artifacts in memory."""
    data_dir = Path(data_dir)
    movies = build_movies(
        str(data_dir / "movies_metadata.csv"),
        str(data_dir / "keywords.csv"),
        str(data_dir / "credits.csv"),
    )
    soup = build_metadata_soup(movies)
    _, matrix = fit_tfidf(soup)
    id_to_row, row_to_id = build_id_index(movies["id"])
    content = {"matrix": matrix, "id_to_row": id_to_row, "row_to_id": row_to_id}

    ratings = load_ratings(str(data_dir / "ratings_small.csv"), str(data_dir / "links.csv"))
    user_to_row, _ = build_index(ratings["userId"])
    movie_to_col, _ = build_index(ratings["movie_id"])
    user_factors, movie_factors = fit_svd(build_matrix(ratings, user_to_row, movie_to_col))
    collab = {
        "user_factors": user_factors,
        "movie_factors": movie_factors,
        "user_to_row": user_to_row,
        "movie_to_col": movie_to_col,
    }
    return content, collab, movies
