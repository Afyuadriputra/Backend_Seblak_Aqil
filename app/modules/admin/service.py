from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.modules.admin.model import Admin
from app.modules.admin.repository import create, update
from app.modules.admin.schema import AdminCreate, AdminPasswordUpdate, AdminUpdate
from app.shared.exceptions import BadRequestException


def create_admin(db: Session, payload: AdminCreate) -> Admin:
    try:
        admin = create(
            db,
            nama_admin=payload.nama_admin,
            email=payload.email,
            kata_sandi=hash_password(payload.kata_sandi),
        )
        db.commit()
        db.refresh(admin)
        return admin
    except IntegrityError as exc:
        db.rollback()
        raise BadRequestException("Email admin sudah digunakan") from exc


def update_profile(db: Session, admin: Admin, payload: AdminUpdate) -> Admin:
    data = payload.model_dump(exclude_unset=True)

    if not data:
        return admin

    try:
        updated = update(db, admin, data)
        db.commit()
        db.refresh(updated)
        return updated
    except IntegrityError as exc:
        db.rollback()
        raise BadRequestException("Email admin sudah digunakan") from exc


def update_password(db: Session, admin: Admin, payload: AdminPasswordUpdate) -> None:
    if not verify_password(payload.kata_sandi_lama, admin.kata_sandi):
        raise BadRequestException("Kata sandi lama salah")

    admin.kata_sandi = hash_password(payload.kata_sandi_baru)
    db.commit()
