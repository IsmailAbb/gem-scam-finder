"""Cheap rule-based pre-filters. Run before sending to the LLM to save tokens
and to give the LLM additional structured context in its prompt."""


def score(snapshot_features: dict) -> dict:
    """Return {'age_days': int, 'has_payment': bool, 'lookalike_score': float, ...}.

    TODO: compute age from WHOIS creation_date, edit-distance to canonical domains,
    presence of payment forms, suspicious TLDs, etc.
    """
    raise NotImplementedError
