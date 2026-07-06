"""Movie catalog endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import Movie, get_db
from app.schemas import MovieDetail, MovieSummary

router = APIRouter()


@router.get("/movies", response_model=list[MovieSummary])
def list_movies(search: str = "", limit: int = 20, db: Session = Depends(get_db)):
    """Return catalog movies, optionally filtered by a title search."""
    query = db.query(Movie)
    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))
    return query.order_by(Movie.title).limit(limit).all()


@router.get("/movies/{movie_id}", response_model=MovieDetail)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Return full detail for one movie, including a link to its IMDb page."""
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="movie not found")
    imdb_url = f"https://www.imdb.com/title/{movie.imdb_id}/" if movie.imdb_id else ""
    return MovieDetail(
        id=movie.id,
        title=movie.title,
        year=movie.year,
        genres=movie.genres,
        overview=movie.overview,
        tagline=movie.tagline,
        cast=movie.cast,
        director=movie.director,
        producers=movie.producers,
        runtime=movie.runtime,
        vote_average=movie.vote_average,
        vote_count=movie.vote_count,
        poster_path=movie.poster_path,
        imdb_url=imdb_url,
    )
