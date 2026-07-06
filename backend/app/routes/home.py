"""Home feed grouped by genre."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import Movie, get_db
from app.schemas import HomeRow, MovieSummary

router = APIRouter()

GENRES = [
    "Action",
    "Comedy",
    "Drama",
    "Adventure",
    "Animation",
    "Science Fiction",
    "Thriller",
    "Romance",
    "Family",
    "Horror",
]


@router.get("/home", response_model=list[HomeRow])
def home_feed(per_genre: int = 12, db: Session = Depends(get_db)):
    """Return a row of popular, poster-backed movies for each home-page genre."""
    rows = []
    for genre in GENRES:
        movies = (
            db.query(Movie)
            .filter(Movie.genres.like(f"%{genre}%"), Movie.poster_path != "")
            .order_by(Movie.vote_count.desc())
            .limit(per_genre)
            .all()
        )
        rows.append(HomeRow(genre=genre, movies=[MovieSummary.model_validate(m) for m in movies]))
    return rows
