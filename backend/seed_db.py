"""Load the movie catalog from the precomputed CSV into the database."""

import pandas as pd

from app.config import CATALOG_PATH
from app.db import Movie, SessionLocal, engine, init_db


def _text(value):
    return value if isinstance(value, str) else ""


def seed(catalog_path=CATALOG_PATH):
    """Recreate the movie table and fill it from the catalog on disk."""
    Movie.__table__.drop(engine, checkfirst=True)
    init_db()
    catalog = pd.read_csv(catalog_path)
    session = SessionLocal()
    try:
        session.bulk_save_objects(
            Movie(
                id=int(row.id),
                title=row.title,
                genres=_text(row.genres),
                year=int(row.year) if pd.notna(row.year) else None,
                overview=_text(row.overview),
                tagline=_text(row.tagline),
                cast=_text(row.cast),
                director=_text(row.director),
                producers=_text(row.producers),
                runtime=int(row.runtime) if pd.notna(row.runtime) else None,
                vote_average=float(row.vote_average) if pd.notna(row.vote_average) else None,
                vote_count=int(row.vote_count) if pd.notna(row.vote_count) else None,
                poster_path=_text(row.poster_path),
                imdb_id=_text(row.imdb_id),
            )
            for row in catalog.itertuples()
        )
        session.commit()
        return session.query(Movie).count()
    finally:
        session.close()


if __name__ == "__main__":
    count = seed()
    print(f"seeded {count} movies")
