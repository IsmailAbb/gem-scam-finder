from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Target(Base):
    """A canonical GEM domain we're protecting against impersonation."""

    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String, unique=True, index=True)
    display_name: Mapped[str]
    notes: Mapped[str | None] = mapped_column(Text, default=None)

    candidates: Mapped[list["Candidate"]] = relationship(back_populates="seed_target")


class Candidate(Base):
    """A domain discovered by any source - may or may not turn out to be a scam."""

    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String, unique=True, index=True)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    source: Mapped[str]  # dnstwist | ct | serp | newdomains | manual
    seed_target_id: Mapped[int | None] = mapped_column(ForeignKey("targets.id"))
    status: Mapped[str] = mapped_column(default="pending")
    # pending → enriched → classified → reviewed → published | dismissed

    seed_target: Mapped["Target | None"] = relationship(back_populates="candidates")
    snapshots: Mapped[list["Snapshot"]] = relationship(back_populates="candidate")


class Snapshot(Base):
    """One capture of a candidate at a point in time - the evidence record."""

    __tablename__ = "snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), index=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    final_url: Mapped[str | None]
    http_status: Mapped[int | None]
    redirect_chain: Mapped[list[str] | None] = mapped_column(JSON)
    screenshot_path: Mapped[str | None]
    html_path: Mapped[str | None]
    whois_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    dns_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    candidate: Mapped["Candidate"] = relationship(back_populates="snapshots")
    classifications: Mapped[list["Classification"]] = relationship(back_populates="snapshot")


class Classification(Base):
    """An LLM verdict on a snapshot."""

    __tablename__ = "classifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshots.id"), index=True)
    model: Mapped[str]
    verdict: Mapped[str]  # benign | suspicious | impersonating | inconclusive
    confidence: Mapped[float]
    evidence_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    rationale: Mapped[str] = mapped_column(Text)
    classified_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    snapshot: Mapped["Snapshot"] = relationship(back_populates="classifications")
    review: Mapped["ReviewDecision | None"] = relationship(back_populates="classification")


class ReviewDecision(Base):
    """A human verdict - overrides the LLM when present."""

    __tablename__ = "review_decisions"

    id: Mapped[int] = mapped_column(primary_key=True)
    classification_id: Mapped[int] = mapped_column(
        ForeignKey("classifications.id"), unique=True
    )
    reviewer: Mapped[str]
    decision: Mapped[str]  # confirm | reject | recapture | defer
    notes: Mapped[str | None] = mapped_column(Text)
    decided_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    classification: Mapped["Classification"] = relationship(back_populates="review")


class PublishedEntry(Base):
    """A candidate published on the public-facing database."""

    __tablename__ = "published_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), unique=True)
    status: Mapped[str] = mapped_column(default="active")
    # active | taken_down | disputed
    evidence_snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshots.id"))
    published_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    removed_at: Mapped[datetime | None]


class AbuseReport(Base):
    """A draft or filed abuse report against a registrar/host/ad-network."""

    __tablename__ = "abuse_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), index=True)
    target_type: Mapped[str]  # registrar | host | ad_network
    target_name: Mapped[str]
    body: Mapped[str] = mapped_column(Text)
    filed_at: Mapped[datetime | None]
    response: Mapped[str | None] = mapped_column(Text)
    resolved_at: Mapped[datetime | None]
