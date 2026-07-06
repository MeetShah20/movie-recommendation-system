"""Load and cache the recommender artifacts."""

from functools import lru_cache

from app.config import ARTIFACTS_DIR
from recommender.artifacts import load_artifacts


@lru_cache(maxsize=1)
def get_models():
    """Return the (content, collab) artifacts, loaded from disk once and cached."""
    return load_artifacts(ARTIFACTS_DIR)
