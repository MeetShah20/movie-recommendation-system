"""Collaborative recommendations from user ratings via latent factors."""

import pandas as pd


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
