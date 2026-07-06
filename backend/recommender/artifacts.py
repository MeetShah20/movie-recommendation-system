"""Load the precomputed recommender artifacts from disk."""

from pathlib import Path

import numpy as np
from scipy.sparse import load_npz


def _index_from_ids(ids):
    """Rebuild an id-to-position map from ids stored in position order."""
    return {int(value): pos for pos, value in enumerate(ids)}


def load_artifacts(directory):
    """Read the persisted artifacts and rebuild the content and collab structures."""
    directory = Path(directory)
    content_ids = [int(i) for i in np.load(directory / "content_ids.npy")]
    content = {
        "matrix": load_npz(directory / "tfidf_matrix.npz"),
        "id_to_row": _index_from_ids(content_ids),
        "row_to_id": content_ids,
    }
    collab = {
        "user_factors": np.load(directory / "user_factors.npy"),
        "movie_factors": np.load(directory / "movie_factors.npy"),
        "user_to_row": _index_from_ids(np.load(directory / "user_ids.npy")),
        "movie_to_col": _index_from_ids(np.load(directory / "collab_movie_ids.npy")),
    }
    return content, collab
