"""Build the Anthropic prompt payload. The rubric is sent as a cached block so we
pay for it only on the first call of a 5-minute window."""

from pathlib import Path

from gemscan.settings import ROOT

RUBRIC_PATH = ROOT / "config" / "rubric.md"


def load_rubric() -> str:
    return RUBRIC_PATH.read_text(encoding="utf-8")


def build_messages(snapshot_summary: dict, screenshot_b64: str) -> list[dict]:
    """Return the `messages` argument for the Anthropic client.

    The system prompt + rubric are sent separately and marked cache_control
    so identical re-prompts get cached pricing.

    TODO: implement actual message construction with vision + structured-output schema.
    """
    raise NotImplementedError
