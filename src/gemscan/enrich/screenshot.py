"""Render the candidate page in headless Chromium and save a screenshot + HTML snapshot."""

from pathlib import Path


def capture(domain: str, out_dir: Path) -> dict:
    """Return {'screenshot_path': Path, 'html_path': Path, 'final_url': str}.

    TODO: use Playwright with playwright-stealth; render at desktop (1280x800) and
    mobile (390x844) viewports; save both screenshots + the full DOM HTML.
    """
    raise NotImplementedError
