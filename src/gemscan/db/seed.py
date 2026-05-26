"""Seed canonical targets from config/targets.yaml into the database."""

import yaml
from sqlalchemy import delete, select

from gemscan.db.models import Candidate, Target
from gemscan.db.session import SessionLocal
from gemscan.settings import ROOT

TARGETS_FILE = ROOT / "config" / "targets.yaml"


def seed_targets() -> dict[str, int]:
    """Reconcile the targets table with config/targets.yaml.

    YAML is the source of truth: rows present in the YAML are inserted
    if missing; rows present in the DB but absent from the YAML are
    removed, along with any Candidates that were generated from them.

    Returns {"added": int, "removed": int}.
    """
    with TARGETS_FILE.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    yaml_targets = {entry["domain"]: entry for entry in data.get("targets", [])}

    added = 0
    removed = 0
    with SessionLocal() as session:
        db_targets = {t.domain: t for t in session.scalars(select(Target)).all()}

        for domain, entry in yaml_targets.items():
            if domain in db_targets:
                continue
            session.add(
                Target(
                    domain=domain,
                    display_name=entry["display_name"],
                    notes=entry.get("notes"),
                )
            )
            added += 1

        for domain, target in db_targets.items():
            if domain in yaml_targets:
                continue
            session.execute(
                delete(Candidate).where(Candidate.seed_target_id == target.id)
            )
            session.delete(target)
            removed += 1

        session.commit()

    return {"added": added, "removed": removed}
