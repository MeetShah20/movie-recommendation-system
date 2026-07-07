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


class RecommendRequest(BaseModel):
    movie_id: int | None = None
    text: str = ""
    genres: list[str] = []
    cast: str = ""
    director: str = ""
    min_rating: float = 0.0
    people: list[int] = []
    top_n: int = 12


class ReasonedMovie(MovieSummary):
    score: float
    reasons: list[str]


class ReasonedResponse(BaseModel):
    results: list[ReasonedMovie]


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


class RegisterRequest(BaseModel):
    username: str
    name: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LikeRequest(BaseModel):
    movie_id: int


class Person(BaseModel):
    kind: str
    id: int
    name: str


class AddFriendRequest(BaseModel):
    kind: str
    id: int
