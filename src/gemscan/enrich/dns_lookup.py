"""Resolve a domain's A/AAAA/NS/MX records — used to identify shared hosting infrastructure."""


def lookup(domain: str) -> dict:
    """Return {'a': [...], 'aaaa': [...], 'ns': [...], 'mx': [...], 'asn': ..., 'host_country': ...}.

    TODO: use dnspython for record lookups; combine with an IP-to-ASN lookup so we
    can group candidates by hosting provider.
    """
    raise NotImplementedError
