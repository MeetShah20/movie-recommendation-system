"""Saving movies to watch later."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import Movie, User, Watchlist, get_db
from app.dependencies import get_current_user
from app.schemas import MovieSummary, WatchlistRequest

router = APIRouter()


@router.post("/watchlist", status_code=204)
def add_to_watchlist(
    payload: WatchlistRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Save a movie to the signed-in user's watchlist."""
    if db.get(Movie, payload.movie_id) is None:
        raise HTTPException(status_code=404, detail="movie not found")
    exists = db.query(Watchlist).filter_by(user_id=user.id, movie_id=payload.movie_id).first()
    if exists is None:
        db.add(Watchlist(user_id=user.id, movie_id=payload.movie_id))
        db.commit()


@router.delete("/watchlist/{movie_id}", status_code=204)
def remove_from_watchlist(
    movie_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Remove a movie from the watchlist."""
    db.query(Watchlist).filter_by(user_id=user.id, movie_id=movie_id).delete()
    db.commit()


@router.get("/watchlist", response_model=list[MovieSummary])
def my_watchlist(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Return the movies on the signed-in user's watchlist."""
    return (
        db.query(Movie)
        .join(Watchlist, Watchlist.movie_id == Movie.id)
        .filter(Watchlist.user_id == user.id)
        .all()
    )
