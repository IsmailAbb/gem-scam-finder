"""Walk every pending Candidate, probe it, capture a screenshot, write a Snapshot row."""

from sqlalchemy import select

from gemscan.db.models import Candidate, Snapshot
from gemscan.db.session import SessionLocal
from gemscan.enrich import http_probe, screenshot
from gemscan.settings import settings


def enrich_pending() -> dict[str, int]:
    """Enrich every Candidate in `pending` status. Returns {captured, dead, total}.

    For each candidate:
      1. HTTP-probe to find the working scheme + redirect chain.
      2. If the probe succeeded, render the final URL in Playwright.
      3. Write a Snapshot row (always — even partial captures preserve evidence).
      4. Advance the candidate to `enriched`.

    Snapshots whose probe failed entirely (no scheme worked) still get a row —
    the absence of evidence is itself evidence. Classification will skip them.
    """
    captured = 0
    dead = 0
    total = 0

    with SessionLocal() as session:
        pending = session.scalars(
            select(Candidate).where(Candidate.status == "pending")
        ).all()

        for candidate in pending:
            total += 1
            print(f"  enriching [{candidate.id}] {candidate.domain}")

            probe_result = http_probe.probe(candidate.domain)

            shot_result: dict = {
                "screenshot_path": None,
                "html_path": None,
                "final_url": None,
                "error": "skipped — probe failed",
            }
            if probe_result["error"] is None:
                out_dir = settings.snapshots_dir / str(candidate.id)
                shot_result = screenshot.capture(probe_result["final_url"], out_dir)

            session.add(
                Snapshot(
                    candidate_id=candidate.id,
                    final_url=shot_result["final_url"] or probe_result["final_url"],
                    http_status=probe_result["http_status"],
                    redirect_chain=probe_result["redirect_chain"] or None,
                    screenshot_path=shot_result["screenshot_path"],
                    html_path=shot_result["html_path"],
                )
            )
            candidate.status = "enriched"

            if shot_result["screenshot_path"] is not None:
                captured += 1
                print(f"    captured -> {shot_result['screenshot_path']}")
            else:
                dead += 1
                err = shot_result["error"] or probe_result["error"]
                print(f"    no capture ({err})")

        session.commit()

    return {"captured": captured, "dead": dead, "total": total}
