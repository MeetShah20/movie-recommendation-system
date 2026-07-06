"""Give the MovieLens users display names and store them as browsable profiles."""

from pathlib import Path

import numpy as np

from app.config import ARTIFACTS_DIR
from app.db import Profile, SessionLocal, engine, init_db

FIRST_NAMES = [
    "Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace", "Henry",
    "Isla", "Jack", "Karen", "Liam", "Maya", "Noah", "Olivia", "Peter",
    "Quinn", "Rachel", "Sam", "Tara", "Umar", "Vera", "Will", "Xena",
    "Yusuf", "Zoe", "Adam", "Bella", "Chris", "Diana",
]

LAST_NAMES = [
    "Adams", "Baker", "Clark", "Dixon", "Evans", "Foster", "Gray", "Hughes",
    "Irving", "Jones", "Kelly", "Lewis", "Morgan", "Nolan", "Owens", "Price",
    "Barnes", "Reed", "Shaw", "Turner", "Underwood", "Vance", "Walsh", "Young",
    "Zimmer", "Brooks", "Cole", "Dean", "Ellis", "Fisher",
]


def _names(count):
    """Return `count` unique 'First Last' names in a fixed order."""
    combos = [f"{first} {last}" for last in LAST_NAMES for first in FIRST_NAMES]
    return combos[:count]


def seed(artifacts_dir=ARTIFACTS_DIR):
    """Recreate the profiles table with one named profile per MovieLens user."""
    Profile.__table__.drop(engine, checkfirst=True)
    init_db()
    user_ids = np.load(Path(artifacts_dir) / "user_ids.npy")
    names = _names(len(user_ids))
    session = SessionLocal()
    try:
        session.bulk_save_objects(
            Profile(movielens_id=int(user_id), name=name)
            for user_id, name in zip(user_ids, names)
        )
        session.commit()
        return session.query(Profile).count()
    finally:
        session.close()


if __name__ == "__main__":
    count = seed()
    print(f"seeded {count} profiles")
