"""FastAPI application factory. Mounts the public site and the auth-gated admin UI."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from gemscan import __version__
from gemscan.api import admin, public

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="GEM Scam Finder",
    version=__version__,
    description="Public database of websites impersonating the Grand Egyptian Museum.",
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(public.router)
app.include_router(admin.router, prefix="/admin")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}
