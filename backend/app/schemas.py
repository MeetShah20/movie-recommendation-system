"""Response models for the API."""

from pydantic import BaseModel, ConfigDict


class MovieSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    genres: str
    year: int | None = None
    poster_path: str = ""
    vote_average: float | None = None


class Recommendation(BaseModel):
    movie_id: int
    title: str
    score: float


class RecommendResponse(BaseModel):
    input_movie: str
    mode_used: str
    recommendations: list[Recommendation]


class MovieDetail(BaseModel):
    id: int
    title: str
    year: int | None = None
    genres: str
    overview: str
    tagline: str
    cast: str
    director: str
    producers: str
    runtime: int | None = None
    vote_average: float | None = None
    vote_count: int | None = None
    poster_path: str
    imdb_url: str


class HomeRow(BaseModel):
    genre: str
    movies: list[MovieSummary]
