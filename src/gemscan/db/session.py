from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gemscan.db.models import Base
from gemscan.settings import settings

engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """Create data directories and all SQL tables if they don't exist yet."""
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.snapshots_dir.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)
