"""Recommendation endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import HYBRID_ALPHA
from app.db import Movie, Profile, get_db
from app.models_store import get_models
from app.recommend_engine import recommend as recommend_v2
from app.schemas import (
    ReasonedMovie,
    ReasonedResponse,
    Recommendation,
    RecommendRequest,
    RecommendResponse,
)
from recommender.hybrid import recommend

router = APIRouter()


@router.get("/recommend", response_model=RecommendResponse)
def recommend_movies(
    movie_id: int,
    user_id: int | None = None,
    top_n: int = 10,
    db: Session = Depends(get_db),
):
    """Recommend movies for a chosen movie, personalized for a user when known."""
    seed = db.get(Movie, movie_id)
    if seed is None:
        raise HTTPException(status_code=404, detail="movie not found")

    content, collab = get_models()
    result = recommend(movie_id, user_id, content, collab, top_n=top_n, alpha=HYBRID_ALPHA)

    recommendations = []
    for rec_id, score in result["recommendations"]:
        movie = db.get(Movie, rec_id)
        if movie is not None:
            recommendations.append(
                Recommendation(movie_id=rec_id, title=movie.title, score=round(score, 4))
            )

    label = f"{seed.title} ({seed.year})" if seed.year else seed.title
    return RecommendResponse(
        input_movie=label, mode_used=result["mode"], recommendations=recommendations
    )


@router.post("/recommend", response_model=ReasonedResponse)
def recommend_from_inputs(payload: RecommendRequest, db: Session = Depends(get_db)):
    """Rank movies from any mix of inputs and tag each with why it was picked."""
    friends = {}
    if payload.people:
        for profile in db.query(Profile).filter(Profile.id.in_(payload.people)).all():
            friends[profile.movielens_id] = profile.name

    content, collab = get_models()
    ranked = recommend_v2(
        db,
        content,
        collab,
        movie_id=payload.movie_id,
        text=payload.text,
        genres=payload.genres,
        cast=payload.cast,
        director=payload.director,
        min_rating=payload.min_rating,
        friends=friends,
        top_n=payload.top_n,
    )

    results = []
    for item in ranked:
        movie = db.get(Movie, item["movie_id"])
        if movie is not None:
            results.append(
                ReasonedMovie(
                    id=movie.id,
                    title=movie.title,
                    genres=movie.genres,
                    year=movie.year,
                    poster_path=movie.poster_path,
                    vote_average=movie.vote_average,
                    score=item["score"],
                    reasons=item["reasons"],
                )
            )
    return ReasonedResponse(results=results)
