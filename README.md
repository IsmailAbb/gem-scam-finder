# GEM Scam Finder

Detects, tracks, and reports websites impersonating the **Grand Egyptian Museum (GEM)** to scam tourists buying tickets online.

> **Status:** Pre-MVP scaffold. The pipeline structure exists; individual stages are stubbed.

## Why this exists

GEM is one of the largest archaeological museums in the world and a top tourist destination. Scammers register look-alike domains (`grandegyptianmusuem.com`, `gem-tickets.shop`, etc.), copy the official site's branding, and take payments for tickets that don't exist. There is currently no systematic public database of these sites for Egypt.

This project aims to be that database, plus the tooling to keep it current.

## How it works

```
 ┌──────────────┐    ┌────────┐    ┌──────────┐    ┌────────┐    ┌─────────┐    ┌────────┐
 │  Discovery   │ -> │ Enrich │ -> │ Classify │ -> │ Review │ -> │ Publish │ -> │ Report │
 └──────────────┘    └────────┘    └──────────┘    └────────┘    └─────────┘    └────────┘
   dnstwist, CT      WHOIS, DNS,    Claude with    Human in       Public DB +    Auto-draft
   logs, SERP,       HTTP probe,    a structured   the loop       JSON API       abuse reports
   new-domain        Playwright     rubric         (admin UI)                    to registrars,
   feeds             screenshot                                                  hosts, ad nets
```

State flows through SQLite. Each stage adds rows, never mutates earlier ones — you keep a full audit trail of why each site was flagged.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```powershell
# Install uv if you don't have it
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# From the project root
uv sync                    # install dependencies into a local venv
uv run playwright install  # download browser binaries (~500 MB, one-time)

# Configure
copy .env.example .env     # then edit .env and add your ANTHROPIC_API_KEY

# Initialize the database and seed canonical targets
uv run gemscan init
```

## Usage

```powershell
uv run gemscan --help          # list all commands
uv run gemscan discover        # find new candidate domains  (stub)
uv run gemscan enrich          # WHOIS + screenshot pending candidates  (stub)
uv run gemscan classify        # send enriched candidates to Claude  (stub)
uv run gemscan serve           # run the web UI on http://127.0.0.1:8000  (stub)
```

## Project layout

```
src/gemscan/
├── cli.py            # Typer entry point — `gemscan <command>`
├── settings.py       # env / config loader
├── db/               # SQLAlchemy models + session
├── discovery/        # find candidate domains
├── enrich/           # gather evidence on each candidate
├── classify/         # Claude-based verdict
├── review/           # human-in-the-loop queue
├── report/           # generate abuse-report drafts
└── api/              # FastAPI web app (public site + admin UI)

config/
├── targets.yaml      # canonical GEM domains to protect
└── rubric.md         # the classification rubric (prose, edited by hand)

data/                 # gitignored — SQLite DB + screenshots
tests/                # pytest tests + recorded fixtures
scripts/              # one-off utilities (seed targets, etc.)
```

## Legal & ethical notes

- This project publishes accusations of fraud against specific domains. Every published entry must be backed by a saved evidence snapshot (screenshot + DOM + WHOIS) and a human review decision.
- Entries are framed as **indicators of suspected impersonation**, not legal conclusions. A "report a mistake" channel is provided.
- Scraping is limited to publicly accessible content. No credentials, no exploitation, no PII submission.
- Abuse reports are filed through standard registrar/host/ad-network channels — the same mechanisms anyone can use.

## License

MIT — see [LICENSE](LICENSE).
