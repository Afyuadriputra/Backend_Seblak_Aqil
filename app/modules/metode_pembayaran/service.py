from pathlib import Path

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.modules.metode_pembayaran import repository
from app.modules.metode_pembayaran.model import MetodePembayaran
from app.modules.metode_pembayaran.schema import (
    MetodePembayaranCreate,
    MetodePembayaranStatusUpdate,
    MetodePembayaranUpdate,
)
from app.shared.exceptions import BadRequestException, NotFoundException
from app.shared.file_validator import generate_safe_filename, validate_file_size

settings = get_settings()


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


def update_gambar_qr(
    db: Session,
    metode_id: int,
    original_filename: str,
    content: bytes,
) -> MetodePembayaran:
    metode = get_metode(db, metode_id)
    validate_file_size(len(content))

    safe_filename = generate_safe_filename(original_filename)
    upload_dir = settings.upload_path / "metode_pembayaran"
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / safe_filename
    old_path = Path(metode.gambar_qr) if metode.gambar_qr else None

    try:
        path.write_bytes(content)
        metode.gambar_qr = str(path)
        db.commit()
        db.refresh(metode)
        if old_path and old_path.exists() and old_path != path:
            old_path.unlink()
        return metode
    except Exception:
        db.rollback()
        if path.exists():
            path.unlink()
        raise


def delete_metode(db: Session, metode_id: int) -> None:
    metode = get_metode(db, metode_id)
    try:
        repository.delete(db, metode)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BadRequestException("Metode pembayaran masih digunakan pesanan") from exc
