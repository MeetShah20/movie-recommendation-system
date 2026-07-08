# Movie Recommendation System

A web application that recommends movies. It can suggest films from a movie you already like, from criteria such as genre, actor, director, or a short description of what you are in the mood for, and from the tastes of people you add as friends. Each recommendation comes with a short reason that explains why it was chosen.

The interface is a dark, Netflix-style site with genre rows on the home page, a detail view for every film, search, and personal accounts that can like movies and keep a watchlist.

## Features

- A home feed of popular movies grouped into genre rows
- A recommendation page that accepts several inputs at once: a seed movie, genres, an actor, a director, a minimum rating, a free-text description, and selected friends
- A reason attached to each recommendation, for example "Comedy film", "Directed by Christopher Nolan", "Matches your description", or "Recommended by Alice Adams"
- A movie detail view with the poster, overview, cast, crew, rating, and a link to the film's IMDb page
- Accounts with sign up and sign in
- Liked movies and a watchlist, each on its own page
- Friends, who can be other registered users or named viewer profiles drawn from the ratings data, whose taste feeds into your recommendations
- Search across the catalogue

## How the recommendations work

Two methods sit behind the suggestions.

The first is content based. Every film is described by its genres, keywords, cast, director, and plot overview. That text is turned into a TF-IDF vector, and the similarity between two films is measured with cosine similarity. This method drives the "similar films" results and the free-text description box.

The second is collaborative. The MovieLens ratings are factorised with a truncated SVD into latent factors for users and films. This method drives the "people who watched this also watched" results and the recommendations that come from a friend's taste.

The recommendation page combines whichever inputs you give it into a single pool of candidate films. Each signal adds a score and a reason to a candidate, the scores are summed so that a film matching more of your inputs ranks higher, and the top films are returned together with their reasons.

The heavy calculations run once in a preparation step and are saved to disk. The API loads these saved artifacts when it starts, which keeps requests fast.

## Tech stack

- Backend and API: Python with FastAPI
- Frontend: React with Vite, served by nginx
- Database: SQLite
- Machine learning: scikit-learn, pandas, and scipy
- Containers: Docker and Docker Compose

## Architecture

The app runs as two containers on a private Docker network. The backend serves the API and loads the precomputed model artifacts. The frontend is the built React site, served as static files by nginx. The database is a SQLite file kept on a named Docker volume, so accounts, likes, watchlists, and friendships survive a restart. On its first start the backend fills the database with the movie catalogue and the viewer profiles.

## Project structure

- backend: the FastAPI service, the recommendation code, the data preparation script, and the precomputed artifacts
- frontend: the React application and its nginx configuration
- docker-compose.yml: runs the backend, the frontend, the shared network, and the database volume together

## Dataset

The app uses The Movies Dataset from Kaggle, compiled by Rounak Banik. It brings together film details from TMDb and user ratings from MovieLens. Poster images are loaded from TMDb.

Link: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

## Documentation

Setup and run instructions are in SETUP.md. A guide to using the application is in USER_MANUAL.md.
