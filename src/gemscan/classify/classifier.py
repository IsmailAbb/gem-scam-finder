"""Call Claude with the prepared prompt + screenshot and parse the structured verdict."""


def classify_snapshot(snapshot_id: int) -> dict:
    """Load a Snapshot, build the prompt, call Claude, write a Classification row.

    Returns {'verdict': str, 'confidence': float, 'evidence': dict, 'rationale': str}.

    TODO: anthropic.Anthropic().messages.create(...) with prompt caching on the rubric;
    parse JSON response; insert Classification row.
    """
    raise NotImplementedError
