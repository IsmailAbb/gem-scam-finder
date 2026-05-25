"""Public, unauthenticated routes — the lookup page and the published-entries API."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def index() -> dict:
    """Landing page. TODO: render index.html.j2 with summary stats."""
    return {"status": "scaffolding — not implemented yet"}


@router.get("/lookup")
def lookup(domain: str) -> dict:
    """Tourist-facing: 'is this domain known to be a scam?'

    TODO: query PublishedEntry by domain; return verdict + evidence summary.
    """
    return {"domain": domain, "status": "scaffolding — not implemented yet"}


@router.get("/domains")
def list_domains(limit: int = 50, offset: int = 0) -> dict:
    """Paginated list of published scam domains.

    TODO: query PublishedEntry joined with Candidate and the evidence Snapshot.
    """
    return {"items": [], "limit": limit, "offset": offset}
