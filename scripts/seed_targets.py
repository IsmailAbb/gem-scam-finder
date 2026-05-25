"""Load canonical targets from config/targets.yaml into the database.

Run via `uv run gemscan init` (which also creates tables) or directly:
    uv run python -m scripts.seed_targets
"""

from pathlib import Path

import yaml

from gemscan.db.models import Target
from gemscan.db.session import SessionLocal

TARGETS_FILE = Path(__file__).resolve().parents[1] / "config" / "targets.yaml"


def seed() -> int:
    """Insert any new canonical targets into the DB. Idempotent. Returns count added."""
    with TARGETS_FILE.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    added = 0
    with SessionLocal() as session:
        for entry in data.get("targets", []):
            exists = session.query(Target).filter_by(domain=entry["domain"]).first()
            if exists:
                continue
            session.add(
                Target(
                    domain=entry["domain"],
                    display_name=entry["display_name"],
                    notes=entry.get("notes"),
                )
            )
            added += 1
        session.commit()
    return added


if __name__ == "__main__":
    n = seed()
    print(f"Added {n} new target(s).")
