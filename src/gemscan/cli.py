"""Command-line entry point: `uv run gemscan <command>`."""

import typer

from gemscan import __version__

app = typer.Typer(
    help="GEM Scam Finder — detect sites impersonating the Grand Egyptian Museum.",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Show the installed version."""
    typer.echo(f"gemscan {__version__}")


@app.command()
def init() -> None:
    """Create the database, ensure data directories exist, and seed canonical targets."""
    from gemscan.db.seed import seed_targets
    from gemscan.db.session import init_db

    init_db()
    result = seed_targets()
    typer.echo(
        f"Database initialized. Targets: +{result['added']} -{result['removed']}."
    )


@app.command()
def discover() -> None:
    """Run the discovery pipeline (dnstwist for now) to find candidate domains."""
    from gemscan.discovery.pipeline import run_discovery

    added = run_discovery()
    typer.echo(f"Discovery complete. {added} new candidate(s) added.")


@app.command()
def enrich() -> None:
    """Gather WHOIS, DNS, HTTP probe, and screenshot for pending candidates."""
    typer.echo("TODO: implement enrichment pipeline")


@app.command()
def classify() -> None:
    """Send enriched candidates to Claude for verdict."""
    typer.echo("TODO: implement classification")


@app.command()
def report() -> None:
    """Generate abuse-report drafts for confirmed impersonating sites."""
    typer.echo("TODO: implement abuse-report generation")


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000, reload: bool = True) -> None:
    """Run the FastAPI web app (public site + admin UI)."""
    import uvicorn

    uvicorn.run("gemscan.api.main:app", host=host, port=port, reload=reload)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
