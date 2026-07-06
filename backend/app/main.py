from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models_store import get_models
from app.routes import movies, recommend


@asynccontextmanager
async def lifespan(app):
    get_models()
    yield


app = FastAPI(title="Movie Recommender", lifespan=lifespan)
app.include_router(movies.router)
app.include_router(recommend.router)


@app.get("/health")
def health():
    return {"status": "ok"}
