"""Send a HEAD/GET to the candidate domain — capture status, redirect chain, headers."""


def probe(domain: str) -> dict:
    """Return {'final_url': str, 'http_status': int, 'redirect_chain': [str], 'headers': {...}}.

    TODO: use httpx with follow_redirects=True and a realistic browser User-Agent.
    Cap timeout to ~15s; record the full redirect chain (the URL history).
    """
    raise NotImplementedError
