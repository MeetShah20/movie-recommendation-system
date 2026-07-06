"""Multi-signal recommendation engine: combine several inputs into one ranked list with reasons."""

import numpy as np

from app.db import Movie
from recommender.collaborative import also_watched, score_for_users
from recommender.content_based import query_movies, similar_movies

POOL_SIZE = 60


def _add(pool, movie_id, signal, score, reason):
    """Record a signal's score and reason for a candidate movie."""
    entry = pool.setdefault(movie_id, {"signals": {}, "reasons": []})
    if score > entry["signals"].get(signal, 0.0):
        entry["signals"][signal] = score
    if reason not in entry["reasons"]:
        entry["reasons"].append(reason)


def _from_movie(pool, db, content, movie_id):
    seed = db.get(Movie, movie_id)
    if seed is None:
        return
    neighbours = similar_movies(
        movie_id, content["matrix"], content["id_to_row"], content["row_to_id"], top_n=POOL_SIZE
    )
    for candidate_id, score in neighbours:
        _add(pool, candidate_id, "content", score, f"Similar to {seed.title}")


def _from_text(pool, content, text):
    matches = query_movies(
        text, content["vectorizer"], content["matrix"], content["row_to_id"], top_n=POOL_SIZE
    )
    for candidate_id, score in matches:
        _add(pool, candidate_id, "text", score, "Matches your description")


def _from_column(pool, db, column, value, signal, reason):
    rows = (
        db.query(Movie)
        .filter(column.ilike(f"%{value}%"), Movie.poster_path != "")
        .order_by(Movie.vote_count.desc())
        .limit(POOL_SIZE)
        .all()
    )
    for movie in rows:
        _add(pool, movie.id, signal, (movie.vote_average or 0.0) / 10.0, reason)


def _from_friends(pool, collab, col_to_movie, friend_ids, top_k=40):
    scores = score_for_users(
        friend_ids, collab["user_factors"], collab["movie_factors"], collab["user_to_row"]
    )
    if scores is None:
        return
    for index in np.argsort(scores)[::-1][:top_k]:
        if scores[index] <= 0:
            break
        _add(pool, int(col_to_movie[index]), "friends", float(scores[index]), "Liked by your friends")


def _from_also_watched(pool, db, collab, col_to_movie, movie_id):
    seed = db.get(Movie, movie_id)
    if seed is None:
        return
    neighbours = also_watched(
        movie_id, collab["movie_factors"], collab["movie_to_col"], col_to_movie, top_n=30
    )
    for candidate_id, score in neighbours:
        _add(pool, candidate_id, "watched", score, f"People who watched {seed.title} also watched this")


def _rank(pool, db, min_rating, top_n):
    if not pool:
        return []
    signals = {signal for entry in pool.values() for signal in entry["signals"]}
    maxima = {
        signal: max((entry["signals"].get(signal, 0.0) for entry in pool.values()), default=1.0) or 1.0
        for signal in signals
    }
    ratings = dict(db.query(Movie.id, Movie.vote_average).filter(Movie.id.in_(pool.keys())).all())
    ranked = []
    for movie_id, entry in pool.items():
        if min_rating and (ratings.get(movie_id) or 0.0) < min_rating:
            continue
        score = sum(value / maxima[signal] for signal, value in entry["signals"].items())
        ranked.append({"movie_id": movie_id, "score": round(score, 4), "reasons": entry["reasons"]})
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:top_n]


def recommend(db, content, collab, *, movie_id=None, text="", genres=None, cast="", director="", min_rating=0.0, friend_ids=None, top_n=12):
    """Build a ranked, reason-tagged recommendation list from any mix of inputs."""
    pool = {}
    col_to_movie = {position: movie_id_ for movie_id_, position in collab["movie_to_col"].items()}
    if movie_id is not None:
        _from_movie(pool, db, content, movie_id)
        _from_also_watched(pool, db, collab, col_to_movie, movie_id)
    if text:
        _from_text(pool, content, text)
    for genre in genres or []:
        _from_column(pool, db, Movie.genres, genre, "genre", f"{genre} film")
    if cast:
        _from_column(pool, db, Movie.cast, cast, "cast", f"Features {cast}")
    if director:
        _from_column(pool, db, Movie.director, director, "director", f"Directed by {director}")
    if friend_ids:
        _from_friends(pool, collab, col_to_movie, friend_ids)
    return _rank(pool, db, min_rating, top_n)
