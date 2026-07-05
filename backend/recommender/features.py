"""Turn the cleaned movie frame into text features for the content model."""

import pandas as pd


def _join_tokens(names):
    """Lowercase each name and remove its spaces so a multi-word name stays one token."""
    return " ".join(name.lower().replace(" ", "") for name in names)


def normalized_fields(movies):
    """Return each content field as normalized text, ready to be combined into a soup.

    Genres, keywords, cast and director become space-free tokens so that, for
    example, "Tom Hanks" is treated as a single term rather than "tom" and
    "hanks". The overview is only lowercased, since its individual words carry
    the signal there.
    """
    fields = pd.DataFrame(index=movies.index)
    fields["genres"] = movies["genres"].apply(_join_tokens)
    fields["keywords"] = movies["keywords"].apply(_join_tokens)
    fields["cast"] = movies["cast"].apply(_join_tokens)
    fields["director"] = movies["director"].apply(lambda name: name.lower().replace(" ", ""))
    fields["overview"] = movies["overview"].str.lower()
    return fields


def build_metadata_soup(movies):
    """Combine the normalized fields into one text column per movie for TF-IDF."""
    fields = normalized_fields(movies)
    soup = (
        fields["genres"] + " " + fields["keywords"] + " " + fields["cast"]
        + " " + fields["director"] + " " + fields["overview"]
    )
    return soup.str.replace(r"\s+", " ", regex=True).str.strip()
