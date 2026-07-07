"""Liking movies and listing your likes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import Like, Movie, User, get_db
from app.dependencies import get_current_user
from app.schemas import LikeRequest, MovieSummary

router = APIRouter()


@router.post("/likes", status_code=204)
def like_movie(
    payload: LikeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Like a movie for the signed-in user."""
    if db.get(Movie, payload.movie_id) is None:
        raise HTTPException(status_code=404, detail="movie not found")
    exists = db.query(Like).filter_by(user_id=user.id, movie_id=payload.movie_id).first()
    if exists is None:
        db.add(Like(user_id=user.id, movie_id=payload.movie_id))
        db.commit()


@router.delete("/likes/{movie_id}", status_code=204)
def unlike_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Remove a like."""
    db.query(Like).filter_by(user_id=user.id, movie_id=movie_id).delete()
    db.commit()


@router.get("/likes", response_model=list[MovieSummary])
def my_likes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Return the movies the signed-in user has liked."""
    return (
        db.query(Movie)
        .join(Like, Like.movie_id == Movie.id)
        .filter(Like.user_id == user.id)
        .all()
    )
