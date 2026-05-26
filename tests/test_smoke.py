"""Smoke tests - verify the scaffold imports cleanly and the CLI is registered."""

from typer.testing import CliRunner

from gemscan import __version__
from gemscan.cli import app


def test_version_constant():
    assert __version__ == "0.1.0"


def test_cli_help_runs():
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "gemscan" in result.stdout.lower() or "GEM" in result.stdout


def test_cli_version_command():
    result = CliRunner().invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_all_packages_importable():
    """If any module has a syntax / import error this test will fail."""
    from gemscan import api, classify, db, discovery, enrich, report, review  # noqa: F401
    from gemscan.api import admin, main, public  # noqa: F401
    from gemscan.db import models, session  # noqa: F401
    from gemscan.discovery import ct_logs, dnstwist_gen, newdomains, pipeline, serp  # noqa: F401
    from gemscan.enrich import dns_lookup, http_probe, pipeline as enrich_pipeline, screenshot, scrape, whois_lookup  # noqa: F401
