#!/bin/sh
set -e

if ! python -c "from app.db import SessionLocal, Movie; import sys; sys.exit(0 if SessionLocal().query(Movie).first() else 1)" 2>/dev/null; then
  echo "Seeding movie catalog and viewer profiles..."
  python seed_db.py
  python seed_profiles.py
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
