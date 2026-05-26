"""Scrape Google / Bing SERPs for tourist-intent queries - catches paid-ad scams that
don't show up via dnstwist (the scam domain may look nothing like the real one)."""


def search_serps(queries: list[str]) -> list[str]:
    """Run each query, return the union of non-canonical domains that appear in results.

    TODO: pick a SERP source (DuckDuckGo HTML is the easiest to scrape; Google requires
    rotating UAs / proxies or a paid API like SerpAPI). Filter out the canonical
    GEM domains. Include Google Ads slots specifically - those are where most scams live.
    """
    raise NotImplementedError
