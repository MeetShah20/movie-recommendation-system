"""Multi-signal recommendation engine: combine several inputs into one ranked list with reasons."""

import numpy as np

from app.db import Movie
from recommender.collaborative import also_watched
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


def _friends_reason(names):
    """Phrase who recommended a movie, listing up to three friends then a '+'."""
    if len(names) == 1:
        return f"Recommended by {names[0]}"
    if len(names) == 2:
        return f"Recommended by {names[0]} and {names[1]}"
    if len(names) == 3:
        return f"Recommended by {names[0]}, {names[1]}, {names[2]}"
    return f"Recommended by {names[0]}, {names[1]}, {names[2]} +"


def _from_friends(pool, collab, col_to_movie, friends, per_friend=30):
    """Add each friend's top picks, naming who recommends each movie."""
    user_to_row = collab["user_to_row"]
    user_factors = collab["user_factors"]
    movie_factors = collab["movie_factors"]
    recommenders = {}
    for movielens_id, name in friends.items():
        if movielens_id not in user_to_row:
            continue
        scores = user_factors[user_to_row[movielens_id]] @ movie_factors.T
        for index in np.argsort(scores)[::-1][:per_friend]:
            if scores[index] <= 0:
                break
            recommenders.setdefault(int(col_to_movie[index]), []).append((name, float(scores[index])))
    for movie_id, backers in recommenders.items():
        backers.sort(key=lambda item: item[1], reverse=True)
        names = [name for name, _ in backers]
        strength = len(backers) + sum(score for _, score in backers) * 0.001
        _add(pool, movie_id, "friends", strength, _friends_reason(names))


def _from_liked(pool, db, content, movie_id):
    """Add movies similar to one the user liked."""
    seed = db.get(Movie, movie_id)
    if seed is None:
        return
    neighbours = similar_movies(
        movie_id, content["matrix"], content["id_to_row"], content["row_to_id"], top_n=POOL_SIZE
    )
    for candidate_id, score in neighbours:
        _add(pool, candidate_id, "liked", score, f"Because you liked {seed.title}")


def _from_friend_likes(pool, friend_likes):
    """Add movies a friend liked, naming who liked each one."""
    for movie_id, names in friend_likes.items():
        strength = len(names) + 0.0005
        _add(pool, movie_id, "friends", strength, _friends_reason(names))


def _from_also_watched(pool, db, collab, col_to_movie, movie_id):
    seed = db.get(Movie, movie_id)
    if seed is None:
        return
    neighbours = also_watched(
        movie_id, collab["movie_factors"], collab["movie_to_col"], col_to_movie, top_n=30
    )
    for candidate_id, score in neighbours:
        _add(pool, candidate_id, "watched", score, f"People who watched {seed.title} also watched this")


def _rank(pool, db, min_rating, top_n, exclude=None):
    if not pool:
        return []
    exclude = exclude or set()
    signals = {signal for entry in pool.values() for signal in entry["signals"]}
    maxima = {
        signal: max((entry["signals"].get(signal, 0.0) for entry in pool.values()), default=1.0) or 1.0
        for signal in signals
    }
    ratings = dict(db.query(Movie.id, Movie.vote_average).filter(Movie.id.in_(pool.keys())).all())
    ranked = []
    for movie_id, entry in pool.items():
        if movie_id in exclude:
            continue
        if min_rating and (ratings.get(movie_id) or 0.0) < min_rating:
            continue
        score = sum(value / maxima[signal] for signal, value in entry["signals"].items())
        ranked.append({"movie_id": movie_id, "score": round(score, 4), "reasons": entry["reasons"]})
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:top_n]


def recommend(db, content, collab, *, movie_id=None, text="", genres=None, cast="", director="", min_rating=0.0, friends=None, liked_ids=None, friend_likes=None, top_n=12):
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
    if friends:
        _from_friends(pool, collab, col_to_movie, friends)
    for liked_id in liked_ids or []:
        _from_liked(pool, db, content, liked_id)
    if friend_likes:
        _from_friend_likes(pool, friend_likes)
    return _rank(pool, db, min_rating, top_n, exclude=set(liked_ids or []))
