import numpy as np
import pytest

from recommender.content_based import fit_tfidf, build_id_index
from recommender.hybrid import blend_scores, recommend


def test_alpha_one_uses_content_only():
    assert blend_scores([1.0, 0.0], [0.0, 1.0], 1.0) == [1.0, 0.0]


def test_alpha_zero_uses_collaborative_only():
    assert blend_scores([1.0, 0.0], [0.0, 1.0], 0.0) == [0.0, 1.0]


def test_missing_collaborative_scores_contribute_nothing():
    assert blend_scores([1.0, 0.0], [None, None], 0.5) == [0.5, 0.0]


@pytest.fixture
def models():
    soups = ["space robot", "space galaxy", "romance love", "romance wedding"]
    ids = [10, 20, 30, 40]
    _, matrix = fit_tfidf(soups)
    id_to_row, row_to_id = build_id_index(ids)
    content = {"matrix": matrix, "id_to_row": id_to_row, "row_to_id": row_to_id}

    collab = {
        "user_factors": np.array([[1.0, 0.0]]),
        "movie_factors": np.array([[0.1, 0.0], [0.9, 0.0], [0.0, 0.5], [0.0, 0.2]]),
        "user_to_row": {1: 0},
        "movie_to_col": {10: 0, 20: 1, 30: 2, 40: 3},
    }
    return content, collab


def test_missing_user_falls_back_to_content(models):
    content, collab = models
    assert recommend(10, None, content, collab, top_n=2)["mode"] == "content"


def test_unknown_user_falls_back_to_content(models):
    content, collab = models
    assert recommend(10, 999, content, collab, top_n=2)["mode"] == "content"


def test_known_user_uses_hybrid(models):
    content, collab = models
    assert recommend(10, 1, content, collab, top_n=2)["mode"] == "hybrid"


def test_result_excludes_query_and_scores_are_floats(models):
    content, collab = models
    result = recommend(10, 1, content, collab, top_n=3)
    assert 10 not in [movie for movie, _ in result["recommendations"]]
    assert all(isinstance(score, float) for _, score in result["recommendations"])
