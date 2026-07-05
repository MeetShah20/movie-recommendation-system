# Data preparation notes

## Source

The data comes from The Movies Dataset on Kaggle (by Rounak Banik):
https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

It combines movie details from TMDb with user ratings from MovieLens. Four files are used:

- movies_metadata.csv - one row per movie with title, overview, genres and more
- keywords.csv - plot keywords per movie
- credits.csv - cast and crew per movie
- ratings_small.csv - user ratings (used later for the collaborative part)

The raw files are not committed to the repository. They go in backend/data/.

## Cleaning steps

movies_metadata.csv has a few rows where the columns are shifted, which leaves a
date string in the id field. The id is converted to a number and those rows are
dropped (three rows). This has to happen before any join, since everything is
joined on id.

The genres, keywords, cast and crew fields are stored as JSON-like text, for
example "[{'id': 18, 'name': 'Drama'}]". These are parsed and reduced to plain
names. For cast only the top three billed actors are kept, and from the crew only
the director.

The three files are joined on id into a single frame. Each file has a few
duplicate ids, so duplicates are removed first to keep one row per movie. The
join is a left join from the movie list, so movies without a matching keyword or
credit row keep empty values instead of being dropped. Missing overviews are
filled with an empty string, and movies without a title are dropped.

The result is one clean row per movie with id, title, overview, genres, keywords,
cast and director. This frame is the input to the feature and recommender steps.
