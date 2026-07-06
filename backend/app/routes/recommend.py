"""Recommendation endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import HYBRID_ALPHA
from app.db import Movie, get_db
from app.models_store import get_models
from app.schemas import Recommendation, RecommendResponse
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
