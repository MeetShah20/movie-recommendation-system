"""Load the movie catalog from the precomputed CSV into the database."""

import pandas as pd

from app.config import CATALOG_PATH
from app.db import Movie, SessionLocal, init_db


def seed(catalog_path=CATALOG_PATH):
    """Create the table and replace its rows with the catalog on disk."""
    init_db()
    catalog = pd.read_csv(catalog_path)
    session = SessionLocal()
    try:
        session.query(Movie).delete()
        session.bulk_save_objects(
            Movie(
                id=int(row.id),
                title=row.title,
                genres=row.genres if isinstance(row.genres, str) else "",
                year=int(row.year) if pd.notna(row.year) else None,
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
