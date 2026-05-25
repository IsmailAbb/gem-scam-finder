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


settings = Settings()
