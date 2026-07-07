from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.db import init_db
from app.models_store import get_models
from app.routes import auth, friends, home, likes, movies, recommend, watchlist


@asynccontextmanager
async def lifespan(app):
    init_db()
    get_models()
    yield


app = FastAPI(title="Movie Recommender", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
app.include_router(movies.router)
app.include_router(recommend.router)
app.include_router(home.router)
app.include_router(auth.router)
app.include_router(friends.router)
app.include_router(likes.router)
app.include_router(watchlist.router)


@app.get("/health")
def health():
    return {"status": "ok"}
