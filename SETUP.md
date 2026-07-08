# Setup and Run

This document explains how to run the application. There are two ways: with Docker, which is the simplest, or locally with the API and the web app started by hand.

## Requirements

- To run with Docker: Docker Desktop, which includes Docker Compose.
- To run locally without Docker: Python 3.12 or newer, and Node.js 20 or newer.

## Run with Docker

From the project root, the folder that holds docker-compose.yml, run:

```
docker compose up --build
```

The first start builds both images and fills the database, so it takes a little while. Once it is ready:

- Web app: http://localhost:8080
- API: http://localhost:8000

To run it in the background, add the detached flag:

```
docker compose up -d --build
```

Stop it with:

```
docker compose down
```

Your accounts, likes, watchlists, and friendships stay in the database volume between runs. To stop and also clear the database, add the volume flag, and the next start will seed it fresh:

```
docker compose down -v
```

All compose commands must be run from the project root.

## Run locally without Docker

The API and the web app run separately, each in its own terminal.

Start the API from the backend folder:

```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed_db.py
python seed_profiles.py
uvicorn app.main:app --reload
```

On macOS or Linux, activate the environment with `source .venv/bin/activate` in place of the Windows activate line.

This serves the API at http://localhost:8000. The two seed steps fill the local database from the catalogue and are only needed the first time.

Start the web app from the frontend folder in a second terminal:

```
cd frontend
npm install
npm run dev
```

This serves the site at http://localhost:5173 and expects the API at http://localhost:8000.

## Environment variables

The defaults are fine for local use. You can override any of them if needed.

Backend:

- DATABASE_URL: where the SQLite database lives. Defaults to a file in the backend folder.
- ALLOWED_ORIGINS: a comma-separated list of sites allowed to call the API. Defaults to http://localhost:5173.
- SECRET_KEY: the key used to sign login tokens. Change it for anything beyond local use.
- ACCESS_TOKEN_TTL_MINUTES: how long a login stays valid. Defaults to 10080, which is seven days.
- ARTIFACTS_DIR: the folder holding the precomputed model files. Defaults to backend/precomputed.

Frontend:

- VITE_API_URL: the API address the web app calls. It is read when the site is built. Defaults to http://localhost:8000.

When running with Docker, these are set in docker-compose.yml. That file is also where the ports 8080 and 8000 are defined, if you need to change them.

## Regenerating the model files

The precomputed model files and the catalogue are already included in the repository, so you do not need this step to run the app. Regenerate them only if you change the raw data or the feature code.

Download The Movies Dataset from Kaggle and place these files in backend/data:

- movies_metadata.csv
- keywords.csv
- credits.csv
- links.csv
- ratings_small.csv

Then, from the backend folder with the environment active, run:

```
python data_prep.py
```

This writes the model files and the catalogue into backend/precomputed. Afterwards, reseed the database with python seed_db.py and python seed_profiles.py.
