from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    pass


def is_sqlite_database(database_url: str) -> bool:
    return database_url.startswith("sqlite")


connect_args = {}
engine_kwargs = {}

if is_sqlite_database(settings.database_url):
    connect_args = {"check_same_thread": False}
else:
    engine_kwargs = {
        "pool_pre_ping": True,
        "pool_recycle": settings.db_pool_recycle_seconds,
        "pool_size": settings.db_pool_size,
        "max_overflow": settings.db_max_overflow,
    }


engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.app_debug and settings.is_development,
    **engine_kwargs,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
