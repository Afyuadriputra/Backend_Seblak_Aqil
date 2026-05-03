from sqlalchemy.orm import Session

from app.modules.admin.model import Admin
from app.modules.admin.repository import get_by_email


def get_admin_by_email(db: Session, email: str) -> Admin | None:
    return get_by_email(db, email)
