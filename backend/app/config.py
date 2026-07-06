"""Application settings, read from the environment with sensible defaults."""

import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BACKEND_DIR / 'movies.db'}")
ARTIFACTS_DIR = Path(os.environ.get("ARTIFACTS_DIR", BACKEND_DIR / "precomputed"))
CATALOG_PATH = ARTIFACTS_DIR / "catalog.csv"
HYBRID_ALPHA = float(os.environ.get("HYBRID_ALPHA", "0.5"))
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me-in-production-please")
ACCESS_TOKEN_TTL_MINUTES = int(os.environ.get("ACCESS_TOKEN_TTL_MINUTES", "10080"))
