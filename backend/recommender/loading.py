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


def load_credits(path, cast_size=3):
    """Read credits.csv and keep the top-billed cast and the director per movie."""
    credits = pd.read_csv(path)
    credits["cast"] = credits["cast"].apply(lambda raw: parse_names(raw, limit=cast_size))
    credits["director"] = credits["crew"].apply(parse_director)
    return credits.drop(columns=["crew"])
