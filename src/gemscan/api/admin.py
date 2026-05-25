"""Admin routes — basic-auth gated. Review queue, publish, file reports."""

import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from gemscan.settings import settings

router = APIRouter()

_security = HTTPBasic()


def require_admin(credentials: HTTPBasicCredentials = Depends(_security)) -> str:
    if not secrets.compare_digest(credentials.password, settings.admin_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/review")
def review_queue(_: str = Depends(require_admin)) -> dict:
    """The next batch of classifications awaiting human review.

    TODO: render an HTML page that shows screenshot, side-by-side with canonical,
    WHOIS, heuristics, LLM rationale, and confirm/reject/recapture buttons.
    """
    return {"status": "scaffolding — not implemented yet"}


@router.post("/publish/{candidate_id}")
def publish(candidate_id: int, _: str = Depends(require_admin)) -> dict:
    """Mark a candidate as confirmed impersonating and publish to the public DB.

    TODO: insert PublishedEntry row referencing the evidence snapshot.
    """
    return {"candidate_id": candidate_id, "status": "scaffolding — not implemented yet"}
