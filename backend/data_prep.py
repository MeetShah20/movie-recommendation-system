"""Build the recommender artifacts once, ready to be written to disk."""

from pathlib import Path

import numpy as np
from scipy.sparse import save_npz

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


def _ordered_ids(index):
    """Return the ids of an index in matrix-position order."""
    return np.array(sorted(index, key=index.get))


def save_artifacts(content, collab, out_dir=ARTIFACTS_DIR):
    """Write the fitted artifacts to disk for the API to load at startup."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    save_npz(out_dir / "tfidf_matrix.npz", content["matrix"])
    np.save(out_dir / "content_ids.npy", np.array(content["row_to_id"]))
    np.save(out_dir / "user_factors.npy", collab["user_factors"])
    np.save(out_dir / "movie_factors.npy", collab["movie_factors"])
    np.save(out_dir / "user_ids.npy", _ordered_ids(collab["user_to_row"]))
    np.save(out_dir / "collab_movie_ids.npy", _ordered_ids(collab["movie_to_col"]))


def save_catalog(movies, out_dir=ARTIFACTS_DIR):
    """Write the slim movie catalog used to seed the database."""
    catalog = movies[["id", "title", "genres", "year"]].copy()
    catalog["genres"] = catalog["genres"].apply(lambda names: ", ".join(names))
    catalog.to_csv(Path(out_dir) / "catalog.csv", index=False)


def main():
    content, collab, movies = build()
    save_artifacts(content, collab)
    save_catalog(movies)
    print(f"wrote artifacts to {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()
