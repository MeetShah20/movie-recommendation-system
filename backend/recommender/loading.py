"""Load and clean the raw movie CSVs."""

import ast

import pandas as pd


def parse_names(raw, limit=None):
    """Pull the name values out of a stringified list of dicts.

    Several columns in this dataset store JSON-like text such as
    "[{'id': 18, 'name': 'Drama'}]". Return the names, or an empty list when
    the value is missing or can't be parsed.
    """
    if not isinstance(raw, str):
        return []
    try:
        items = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return []
    names = [item["name"] for item in items if isinstance(item, dict) and "name" in item]
    return names[:limit] if limit else names


def load_movies(path):
    """Read movies_metadata.csv, drop rows with a bad id, and parse the genres.

    A handful of rows in this file are shifted by one column, which leaves a
    date string in the id field. Coercing to numeric and dropping the misses
    removes them before anything downstream tries to join on id.
    """
    movies = pd.read_csv(path, low_memory=False)
    movies["id"] = pd.to_numeric(movies["id"], errors="coerce")
    movies = movies.dropna(subset=["id"])
    movies["id"] = movies["id"].astype(int)
    movies["genres"] = movies["genres"].apply(parse_names)
    return movies


def load_keywords(path):
    """Read keywords.csv and parse the plot keywords for each movie."""
    keywords = pd.read_csv(path)
    keywords["keywords"] = keywords["keywords"].apply(parse_names)
    return keywords


def parse_director(raw):
    """Return the director's name from a stringified crew list, or '' if absent."""
    if not isinstance(raw, str):
        return ""
    try:
        crew = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return ""
    for member in crew:
        if isinstance(member, dict) and member.get("job") == "Director":
            return member.get("name", "")
    return ""


def parse_producers(raw, limit=2):
    """Return up to `limit` producer names from a stringified crew list."""
    if not isinstance(raw, str):
        return []
    try:
        crew = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return []
    names = [
        member["name"]
        for member in crew
        if isinstance(member, dict) and member.get("job") == "Producer" and "name" in member
    ]
    return names[:limit]


def load_credits(path, cast_size=3):
    """Read credits.csv and keep the top-billed cast, director and producers per movie."""
    credits = pd.read_csv(path)
    credits["cast"] = credits["cast"].apply(lambda raw: parse_names(raw, limit=cast_size))
    credits["director"] = credits["crew"].apply(parse_director)
    credits["producers"] = credits["crew"].apply(parse_producers)
    return credits.drop(columns=["crew"])


def _as_list(value):
    return value if isinstance(value, list) else []


def build_movies(movies_path, keywords_path, credits_path):
    """Join metadata, keywords and credits into one frame keyed by movie id.

    Each source has a few duplicate ids, so they are de-duplicated before the
    join to keep it one row per movie. Movies without a matching keyword or
    credit row keep empty values rather than being dropped.
    """
    columns = [
        "id", "title", "overview", "genres", "release_date",
        "poster_path", "tagline", "runtime", "vote_average", "vote_count", "imdb_id",
    ]
    movies = load_movies(movies_path)[columns]
    movies = movies.dropna(subset=["title"]).drop_duplicates(subset="id")
    keywords = load_keywords(keywords_path).drop_duplicates(subset="id")
    credits = load_credits(credits_path).drop_duplicates(subset="id")

    combined = movies.merge(keywords, on="id", how="left").merge(credits, on="id", how="left")
    combined["overview"] = combined["overview"].fillna("")
    combined["director"] = combined["director"].fillna("")
    combined["tagline"] = combined["tagline"].fillna("")
    combined["poster_path"] = combined["poster_path"].fillna("")
    combined["imdb_id"] = combined["imdb_id"].fillna("")
    combined["runtime"] = combined["runtime"].fillna(0)
    combined["vote_average"] = combined["vote_average"].fillna(0.0)
    combined["vote_count"] = combined["vote_count"].fillna(0)
    combined["keywords"] = combined["keywords"].apply(_as_list)
    combined["cast"] = combined["cast"].apply(_as_list)
    combined["producers"] = combined["producers"].apply(_as_list)
    combined["year"] = pd.to_datetime(combined["release_date"], errors="coerce").dt.year.astype("Int64")
    return combined.drop(columns=["release_date"]).reset_index(drop=True)
