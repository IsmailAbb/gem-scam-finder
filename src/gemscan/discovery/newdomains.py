"""Pull the daily newly-registered-domains feed and grep for brand-relevant strings."""


def newly_registered_matching(keywords: list[str]) -> list[str]:
    """Return today's freshly registered domains that contain any of the keywords.

    TODO: fetch the whoisds.com daily list, decompress, filter by keywords.
    """
    raise NotImplementedError
