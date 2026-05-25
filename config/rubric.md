# Classification Rubric — GEM Impersonation Detection

You are evaluating whether a candidate website is impersonating the **Grand Egyptian Museum (GEM)** in order to defraud tourists buying tickets.

The official GEM presence lives at the domains listed in `config/targets.yaml`. Any other site that pretends to be the GEM or sells GEM tickets while not affiliated with it is suspect.

## Output schema

Respond with valid JSON only, matching this shape:

```json
{
  "verdict": "benign | suspicious | impersonating | inconclusive",
  "confidence": 0.0,
  "evidence": {
    "uses_gem_branding": true,
    "uses_gem_logo": true,
    "sells_tickets_or_takes_payment": true,
    "claims_official_status": false,
    "domain_visually_similar_to_canonical": true,
    "language_targets_tourists": true,
    "other_signals": ["short list of strings"]
  },
  "rationale": "one paragraph explaining the verdict"
}
```

## Verdict definitions

- **impersonating** — The site is clearly trying to pass itself off as the official GEM or as an authorized ticketing partner. High-confidence signals: copied logo + checkout form + lookalike domain + recent registration.
- **suspicious** — Some impersonation signals are present but evidence is partial. Examples: GEM-branded landing page with no checkout, or a legitimate-looking travel agency using GEM imagery in an ambiguous way.
- **benign** — A legitimate site that mentions GEM in passing (news article, blog post, real licensed tour operator) without trying to look like the museum itself.
- **inconclusive** — Page didn't load, was cloaked, was in a language you couldn't read confidently, or evidence is too thin to call either way. Request a recapture.

## Signals to weigh

**Strong evidence of impersonation:**
1. Uses the GEM name and logo prominently above the fold.
2. Has a ticket-purchase or checkout flow asking for credit card / payment data.
3. Domain is visually similar to a canonical GEM domain (typo, homoglyph, keyword stuffing).
4. Domain age is short (< 90 days — provided in the WHOIS data).
5. Hosted on a provider commonly used by scam operations (bulletproof hosts, recently abused ranges).
6. Claims "official" status without authorization.
7. Page is in English/Arabic and clearly targets tourist intent.

**Counter-evidence (pushes toward benign):**
1. Long-established domain (multi-year registration).
2. Clearly identifies itself as a third-party agency, not the museum.
3. Links back to the canonical GEM site honestly.
4. No payment flow — purely informational.
5. Press / blog / educational content.

## Edge cases

- A licensed third-party reseller is **not** impersonating, even if it sells tickets — unless it falsely claims to be the museum itself.
- A scraper / aggregator that mirrors GEM info without a payment flow is at most **suspicious**, not impersonating.
- A site in a language you can't evaluate confidently → **inconclusive**, not a guess.
- Cloaking detected (e.g. only a blank page or 404 captured but the domain has signs of life elsewhere) → **inconclusive**, request recapture.

## Calibration

- Use the full 0.0–1.0 confidence range. Don't anchor to 0.5 or 0.9.
- A verdict of **impersonating** with confidence < 0.85 should be rare — it means you saw most but not all of the strong signals.
- When unsure between **suspicious** and **impersonating**, prefer **suspicious** and let a human reviewer escalate.
