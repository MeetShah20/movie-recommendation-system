import pytest

from recommender.content_based import fit_tfidf, build_id_index, similar_movies


@pytest.fixture
def model():
    soups = [
        "space robot future",
        "space robot galaxy",
        "romance paris love",
        "romance paris wedding",
    ]
    ids = [1, 2, 3, 4]
    _, matrix = fit_tfidf(soups)
    id_to_row, row_to_id = build_id_index(ids)
    return matrix, id_to_row, row_to_id


def test_returns_requested_number(model):
    matrix, id_to_row, row_to_id = model
    results = similar_movies(1, matrix, id_to_row, row_to_id, top_n=2)
    assert len(results) == 2


def test_excludes_the_query_movie(model):
    matrix, id_to_row, row_to_id = model
    results = similar_movies(1, matrix, id_to_row, row_to_id, top_n=3)
    assert 1 not in [movie for movie, _ in results]


def test_closest_match_shares_the_theme(model):
    matrix, id_to_row, row_to_id = model
    top_id, _ = similar_movies(1, matrix, id_to_row, row_to_id, top_n=1)[0]
    assert top_id == 2


def test_unknown_movie_raises(model):
    matrix, id_to_row, row_to_id = model
    with pytest.raises(KeyError):
        similar_movies(999, matrix, id_to_row, row_to_id)
