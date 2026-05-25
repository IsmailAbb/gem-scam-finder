"""Orchestrate all discovery sources into a unified candidate queue."""


def run_discovery() -> int:
    """Run every enabled discovery source, dedupe, and insert new Candidate rows.

    Returns the number of new candidates added.

    TODO: load targets.yaml, fan out to each discovery module, dedupe against
    existing Candidate rows, insert the new ones with source tagging.
    """
    raise NotImplementedError
