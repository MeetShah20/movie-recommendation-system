"""Movie catalog endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import Movie, get_db
from app.schemas import MovieSummary

router = APIRouter()


@router.get("/movies", response_model=list[MovieSummary])
def list_movies(search: str = "", limit: int = 20, db: Session = Depends(get_db)):
    """Return catalog movies, optionally filtered by a title search."""
    query = db.query(Movie)
    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))
    return query.order_by(Movie.title).limit(limit).all()
