"""Seed canonical targets from config/targets.yaml into the database."""

import yaml

from gemscan.db.models import Target
from gemscan.db.session import SessionLocal
from gemscan.settings import ROOT

TARGETS_FILE = ROOT / "config" / "targets.yaml"


def seed_targets() -> int:
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
