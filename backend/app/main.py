from fastapi import FastAPI

from app.routes import movies

app = FastAPI(title="Movie Recommender")
app.include_router(movies.router)


@app.get("/health")
def health():
    return {"status": "ok"}
