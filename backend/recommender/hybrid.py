"""Hybrid recommendations: blend content similarity with collaborative signal."""

from .collaborative import score_movies
from .content_based import similar_movies


def _normalize(scores):
    """Scale scores to 0..1. None values (no signal) map to 0, as do all-equal sets."""
    present = [s for s in scores if s is not None]
    if not present:
        return [0.0 for _ in scores]
    low, high = min(present), max(present)
    if high == low:
        return [0.0 for _ in scores]
    return [0.0 if s is None else (s - low) / (high - low) for s in scores]


def blend_scores(content_scores, collab_scores, alpha):
    """Combine normalized content and collaborative scores with weight alpha.

    Both sides are scaled to 0..1 first because content cosine values and
    collaborative latent scores live on different ranges. Candidates with no
    collaborative score (movie absent from the ratings) contribute 0 on that side.
    """
    content_norm = _normalize(content_scores)
    collab_norm = _normalize(collab_scores)
    return [alpha * c + (1 - alpha) * cf for c, cf in zip(content_norm, collab_norm)]


def content_candidates(movie_id, content, pool_size):
    """Content neighbours of the query movie, used as the candidate pool to re-rank."""
    return similar_movies(
        movie_id, content["matrix"], content["id_to_row"], content["row_to_id"], top_n=pool_size
    )


def recommend(movie_id, user_id, content, collab, top_n=10, alpha=0.5, pool_size=100):
    """Recommend movies similar to movie_id, personalized for user_id.

    A pool of content neighbours is scored for the user with the collaborative
    model, and the two signals are blended. Returns the mode used and the ranked
    (movie_id, score) pairs.
    """
    candidates = content_candidates(movie_id, content, pool_size)
    candidate_ids = [movie for movie, _ in candidates]
    content_scores = [score for _, score in candidates]

    if user_id is None or user_id not in collab["user_to_row"]:
        top = candidates[:top_n]
        return {"mode": "content", "recommendations": [(movie, float(score)) for movie, score in top]}

    user_scores = score_movies(
        user_id, collab["user_factors"], collab["movie_factors"], collab["user_to_row"]
    )
    movie_to_col = collab["movie_to_col"]
    collab_scores = [
        user_scores[movie_to_col[movie]] if movie in movie_to_col else None
        for movie in candidate_ids
    ]

    blended = blend_scores(content_scores, collab_scores, alpha)
    ranked = sorted(zip(candidate_ids, blended), key=lambda pair: pair[1], reverse=True)[:top_n]
    return {"mode": "hybrid", "recommendations": [(movie, float(score)) for movie, score in ranked]}
