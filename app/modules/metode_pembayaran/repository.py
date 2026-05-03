from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.metode_pembayaran.model import MetodePembayaran


def count_all(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(MetodePembayaran)) or 0


def list_all(db: Session, offset: int = 0, limit: int = 20) -> list[MetodePembayaran]:
    return list(
        db.scalars(
            select(MetodePembayaran).order_by(MetodePembayaran.id).offset(offset).limit(limit)
        )
    )


def list_active(db: Session) -> list[MetodePembayaran]:
    return list(
        db.scalars(
            select(MetodePembayaran)
            .where(MetodePembayaran.status_aktif.is_(True))
            .order_by(MetodePembayaran.id)
        )
    )


def get_by_id(db: Session, metode_id: int) -> MetodePembayaran | None:
    return db.get(MetodePembayaran, metode_id)


def create(db: Session, data: dict) -> MetodePembayaran:
    metode = MetodePembayaran(**data)
    db.add(metode)
    db.flush()
    return metode


def update(db: Session, metode: MetodePembayaran, data: dict) -> MetodePembayaran:
    for key, value in data.items():
        setattr(metode, key, value)
    db.flush()
    return metode


def delete(db: Session, metode: MetodePembayaran) -> None:
    db.delete(metode)
    db.flush()
