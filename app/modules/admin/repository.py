from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.admin.model import Admin


def get_by_id(db: Session, admin_id: int) -> Admin | None:
    return db.get(Admin, admin_id)


def get_by_email(db: Session, email: str) -> Admin | None:
    return db.scalar(select(Admin).where(Admin.email == email))


def create(
    db: Session,
    nama_admin: str,
    email: str,
    kata_sandi: str,
    role: str = "admin",
    is_active: bool = True,
) -> Admin:
    admin = Admin(
        nama_admin=nama_admin,
        email=email,
        kata_sandi=kata_sandi,
        role=role,
        is_active=is_active,
    )
    db.add(admin)
    db.flush()
    return admin


def update(db: Session, admin: Admin, data: dict) -> Admin:
    for key, value in data.items():
        setattr(admin, key, value)
    db.flush()
    return admin
