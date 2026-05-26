"""Render the candidate page in headless Chromium and save a screenshot + HTML snapshot."""

from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

from gemscan.settings import settings

VIEWPORT = {"width": 1280, "height": 800}


def capture(url: str, out_dir: Path) -> dict:
    """Render `url` in headless Chromium and persist the evidence.

    Writes `desktop.png` (full-page screenshot) and `dom.html` (rendered HTML
    after JS runs) into `out_dir`. The caller is responsible for choosing the
    URL - typically the `final_url` returned by `http_probe.probe()`.

    Returns:
        screenshot_path: str | None
        html_path: str | None
        final_url: str | None  - `page.url` after JS-driven redirects (may
            differ from the input URL if the page itself navigates)
        error: str | None
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = out_dir / "desktop.png"
    html_path = out_dir / "dom.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                user_agent=settings.user_agent,
                viewport=VIEWPORT,
            )
            page = context.new_page()

            try:
                page.goto(
                    url,
                    timeout=settings.playwright_nav_timeout_ms,
                    wait_until="domcontentloaded",
                )
            except PlaywrightTimeout as e:
                return _failure(f"goto timeout: {e}")
            except Exception as e:
                return _failure(f"goto failed: {type(e).__name__}: {e}")

            # Best-effort: let JS settle. Most SPAs render in <2s but stragglers
            # can keep XHRing forever - don't fail the capture over that.
            try:
                page.wait_for_load_state(
                    "networkidle",
                    timeout=settings.playwright_idle_timeout_ms,
                )
            except PlaywrightTimeout:
                pass

            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                html_path.write_text(page.content(), encoding="utf-8")
            except Exception as e:
                return _failure(f"capture failed: {type(e).__name__}: {e}")

            # Chromium can land on about:blank#blocked, chrome-error://..., etc.
            # when Safe Browsing or a renderer crash interrupts navigation.
            # Those pseudo-URLs are useless for downstream evidence - fall back
            # to what we asked it to load.
            final_url = page.url
            if final_url.startswith(("about:", "chrome-error:")) or not final_url:
                final_url = url

            return {
                "screenshot_path": str(screenshot_path),
                "html_path": str(html_path),
                "final_url": final_url,
                "error": None,
            }
        finally:
            browser.close()


def _failure(message: str) -> dict:
    return {
        "screenshot_path": None,
        "html_path": None,
        "final_url": None,
        "error": message,
    }
