"""Generate look-alike domain permutations from canonical targets using dnstwist."""


def generate_permutations(seed_domain: str) -> list[str]:
    """Return registered look-alike domains for the given seed.

    TODO: invoke dnstwist programmatically, filter by which permutations
    actually resolve in DNS, and return the live ones.
    """
    raise NotImplementedError
