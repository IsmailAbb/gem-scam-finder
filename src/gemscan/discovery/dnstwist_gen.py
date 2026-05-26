"""Generate look-alike domain permutations from canonical targets using dnstwist."""

import dnstwist

ORIGINAL_FUZZER = "*original"


def generate_permutations(
    seed_domain: str,
    threads: int = 50,
) -> list[dict[str, str]]:
    """Return DNS-resolving look-alike domains for the given seed.

    Each result is `{"domain": str, "fuzzer": str}`. The seed itself is
    excluded - only impersonators are returned. Only domains that actually
    resolve in DNS pass through (dnstwist's `registered=True` filter), so
    each result is a candidate worth fetching and classifying.

    `fuzzer` records the permutation strategy that produced the domain
    (e.g. "homoglyph", "omission", "tld-swap", "addition"). Useful for
    analytics on which permutation styles attackers favour against GEM.

    This is a blocking, network-bound call - a typical seed yields a few
    thousand permutations and dnstwist DNS-probes each one. Expect runtimes
    on the order of 30s-3min depending on the threads setting and your
    upstream resolver.
    """
    results = dnstwist.run(
        domain=seed_domain,
        registered=True,
        threads=threads,
        format="null",
    )
    return [
        {"domain": r["domain"], "fuzzer": r["fuzzer"]}
        for r in (results or [])
        if r.get("fuzzer") != ORIGINAL_FUZZER
    ]
