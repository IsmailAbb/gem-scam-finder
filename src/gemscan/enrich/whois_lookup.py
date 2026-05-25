"""Look up WHOIS registration data for a domain. Age is the single highest-signal field."""


def lookup(domain: str) -> dict:
    """Return a normalized WHOIS dict: registrar, creation_date, expiration_date, country, etc.

    TODO: use python-whois; normalize date fields (it returns lists sometimes); handle
    privacy-redacted registrants gracefully.
    """
    raise NotImplementedError
