"""Hybrid recommendations: blend content similarity with collaborative signal."""


def _normalize(scores):
    """Scale scores to 0..1. None values (no signal) map to 0, as do all-equal sets."""
    present = [s for s in scores if s is not None]
    if not present:
        return [0.0 for _ in scores]
    low, high = min(present), max(present)
    if high == low:
        return [0.0 for _ in scores]
    return [0.0 if s is None else (s - low) / (high - low) for s in scores]


def blend_scores(content_scores, collab_scores, alpha):
    """Combine normalized content and collaborative scores with weight alpha.

    Both sides are scaled to 0..1 first because content cosine values and
    collaborative latent scores live on different ranges. Candidates with no
    collaborative score (movie absent from the ratings) contribute 0 on that side.
    """
    content_norm = _normalize(content_scores)
    collab_norm = _normalize(collab_scores)
    return [alpha * c + (1 - alpha) * cf for c, cf in zip(content_norm, collab_norm)]
