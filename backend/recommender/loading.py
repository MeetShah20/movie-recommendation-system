"""Load and clean the raw movie CSVs."""

import pandas as pd


def load_movies(path):
    """Read movies_metadata.csv and drop rows whose id is not a valid integer.

    A handful of rows in this file are shifted by one column, which leaves a
    date string in the id field. Coercing to numeric and dropping the misses
    removes them before anything downstream tries to join on id.
    """
    movies = pd.read_csv(path, low_memory=False)
    movies["id"] = pd.to_numeric(movies["id"], errors="coerce")
    movies = movies.dropna(subset=["id"])
    movies["id"] = movies["id"].astype(int)
    return movies
