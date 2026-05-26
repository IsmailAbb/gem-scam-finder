from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    anthropic_api_key: str | None = None
    admin_password: str = "change-me"

    database_url: str = f"sqlite:///{(ROOT / 'data' / 'gemscan.db').as_posix()}"
    data_dir: Path = ROOT / "data"
    snapshots_dir: Path = ROOT / "data" / "snapshots"

    classification_model: str = "claude-sonnet-4-6"
    escalation_model: str = "claude-opus-4-7"
    review_required_threshold: float = 0.7

    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    http_timeout_seconds: float = 15.0
    playwright_nav_timeout_ms: int = 30_000
    playwright_idle_timeout_ms: int = 10_000


settings = Settings()
