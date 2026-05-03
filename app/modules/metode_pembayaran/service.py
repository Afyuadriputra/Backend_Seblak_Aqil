from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.metode_pembayaran import repository
from app.modules.metode_pembayaran.model import MetodePembayaran
from app.modules.metode_pembayaran.schema import (
    MetodePembayaranCreate,
    MetodePembayaranStatusUpdate,
    MetodePembayaranUpdate,
)
from app.shared.exceptions import BadRequestException, NotFoundException


def list_metode(
    db: Session,
    offset: int = 0,
    limit: int = 20,
) -> tuple[list[MetodePembayaran], int]:
    return repository.list_all(db, offset, limit), repository.count_all(db)


def list_metode_aktif(db: Session) -> list[MetodePembayaran]:
    return repository.list_active(db)


def get_metode(db: Session, metode_id: int) -> MetodePembayaran:
    metode = repository.get_by_id(db, metode_id)
    if metode is None:
        raise NotFoundException("Metode pembayaran tidak ditemukan")
    return metode


def create_metode(db: Session, payload: MetodePembayaranCreate) -> MetodePembayaran:
    metode = repository.create(db, payload.model_dump())
    db.commit()
    db.refresh(metode)
    return metode


def update_metode(
    db: Session,
    metode_id: int,
    payload: MetodePembayaranUpdate,
) -> MetodePembayaran:
    metode = get_metode(db, metode_id)
    data = payload.model_dump(exclude_unset=True)
    metode = repository.update(db, metode, data)
    db.commit()
    db.refresh(metode)
    return metode


def update_status(
    db: Session,
    metode_id: int,
    payload: MetodePembayaranStatusUpdate,
) -> MetodePembayaran:
    metode = get_metode(db, metode_id)
    metode = repository.update(db, metode, {"status_aktif": payload.status_aktif})
    db.commit()
    db.refresh(metode)
    return metode


def delete_metode(db: Session, metode_id: int) -> None:
    metode = get_metode(db, metode_id)
    try:
        repository.delete(db, metode)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BadRequestException("Metode pembayaran masih digunakan pesanan") from exc
