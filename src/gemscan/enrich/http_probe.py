"""Send a GET to the candidate domain — capture status, redirect chain, headers."""

import httpx

from gemscan.settings import settings


def probe(domain: str) -> dict:
    """Return a dict describing what happened when we hit the candidate.

    Keys:
        final_url: str | None  — URL after redirects (None if unreachable)
        http_status: int | None
        redirect_chain: list[str] — every URL we touched, in order
        headers: dict[str, str]
        scheme: 'https' | 'http' | None — which scheme succeeded
        error: str | None — exception summary if both schemes failed

    Tries HTTPS first, falls back to HTTP on connection failure. A 4xx/5xx
    response is still a success (we got an answer); only connect-level
    errors trigger the fallback.
    """
    headers = {"User-Agent": settings.user_agent}
    last_error: str | None = None

    for scheme in ("https", "http"):
        try:
            with httpx.Client(
                headers=headers,
                follow_redirects=True,
                timeout=settings.http_timeout_seconds,
            ) as client:
                response = client.get(f"{scheme}://{domain}")
        except (httpx.HTTPError, httpx.InvalidURL) as e:
            last_error = f"{type(e).__name__}: {e}"
            continue

        chain = [str(r.url) for r in response.history] + [str(response.url)]
        return {
            "final_url": str(response.url),
            "http_status": response.status_code,
            "redirect_chain": chain,
            "headers": dict(response.headers),
            "scheme": scheme,
            "error": None,
        }

    return {
        "final_url": None,
        "http_status": None,
        "redirect_chain": [],
        "headers": {},
        "scheme": None,
        "error": last_error,
    }
