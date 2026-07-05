from fastapi import FastAPI

app = FastAPI(title="Movie Recommender")


@app.get("/health")
def health():
    return {"status": "ok"}
