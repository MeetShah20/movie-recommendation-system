from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.models_store import get_models
from app.routes import auth, home, movies, recommend


@asynccontextmanager
async def lifespan(app):
    get_models()
    yield


app = FastAPI(title="Movie Recommender", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.include_router(movies.router)
app.include_router(recommend.router)
app.include_router(home.router)
app.include_router(auth.router)


@app.get("/health")
def health():
    return {"status": "ok"}
