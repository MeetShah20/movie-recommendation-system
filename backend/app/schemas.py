"""Response models for the API."""

from pydantic import BaseModel, ConfigDict


class MovieSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    genres: str
    year: int | None = None


class Recommendation(BaseModel):
    movie_id: int
    title: str
    score: float


class RecommendResponse(BaseModel):
    input_movie: str
    mode_used: str
    recommendations: list[Recommendation]
