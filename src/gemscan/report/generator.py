"""Generate abuse-report drafts to send to registrars, hosts, and ad networks."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent / "templates"

_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=False)


def render(template_name: str, context: dict) -> str:
    """Render a Jinja template (e.g. 'registrar.j2') with the given context."""
    return _env.get_template(template_name).render(**context)


def draft_for_candidate(candidate_id: int) -> list[dict]:
    """Produce one report draft per relevant authority (registrar / host / ad network).

    TODO: load Candidate + evidence Snapshot, determine which authorities apply
    (registrar from WHOIS, host ASN from DNS, etc.), render each template, persist
    as AbuseReport rows in 'draft' state.
    """
    raise NotImplementedError
