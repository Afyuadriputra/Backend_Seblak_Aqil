from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import SessionLocal, get_db, is_sqlite_database


def test_database_url_is_sqlite():
    settings = get_settings()

    assert is_sqlite_database(settings.database_url) is True


def test_session_local_can_create_session():
    db = SessionLocal()

    try:
        assert isinstance(db, Session)
    finally:
        db.close()


def test_get_db_yields_session():
    db_generator = get_db()
    db = next(db_generator)

    try:
        assert isinstance(db, Session)
    finally:
        try:
            next(db_generator)
        except StopIteration:
            pass
