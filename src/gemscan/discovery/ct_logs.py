"""Poll Certificate Transparency logs (crt.sh) for newly issued certs matching brand patterns."""


def search_ct(pattern: str) -> list[str]:
    """Query crt.sh for certs whose CN/SAN matches the pattern. Return distinct hostnames.

    TODO: hit https://crt.sh/?q=<pattern>&output=json, dedupe, return wildcard-stripped hosts.
    """
    raise NotImplementedError
