"""Orchestrate all discovery sources into a unified candidate queue."""

from sqlalchemy import select

from gemscan.db.models import Candidate, Target
from gemscan.db.session import SessionLocal
from gemscan.discovery import dnstwist_gen

target_domains = ["https://tickets.gem.eg/"]


def run_discovery() -> int:
    """Walk every Target, run each discovery source against it, dedupe against
    existing Candidates, and insert the new ones. Returns count added.

    Currently runs dnstwist only. CT logs, SERP, and new-domain feeds are
    scaffolded but wired in during Milestone 2.
    """
    with SessionLocal() as session:
        targets = session.scalars(select(Target)).all()
        if not targets:
            print("No targets seeded. Run `gemscan init` first.")
            return 0

        existing_domains: set[str] = set(
            session.scalars(select(Candidate.domain)).all()
        )

        total_added = 0
        for target in targets:
            print(f"  scanning {target.domain}... (1-3 min)")
            perms = dnstwist_gen.generate_permutations(target.domain)
            added = 0
            for perm in perms:
                domain = perm["domain"]
                if domain in existing_domains:
                    continue
                session.add(
                    Candidate(
                        domain=domain,
                        source=f"dnstwist:{perm['fuzzer']}",
                        seed_target_id=target.id,
                        status="pending",
                    )
                )
                existing_domains.add(domain)
                added += 1
            print(f"    {len(perms)} look-alike(s), {added} new")
            total_added += added

        session.commit()
    return total_added
