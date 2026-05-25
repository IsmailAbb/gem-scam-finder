"""What surfaces in the admin review UI, in what order."""


def pending_for_review(limit: int = 25) -> list[dict]:
    """Return the next batch of classifications that need human review.

    Priority: high-confidence 'impersonating' first, then borderline 'suspicious'.

    TODO: query Classifications where no ReviewDecision exists, joined with
    Snapshot + Candidate, ordered by (verdict priority, confidence DESC).
    """
    raise NotImplementedError
