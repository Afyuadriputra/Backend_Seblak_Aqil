from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.kategori.model import Kategori


def count_all(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(Kategori)) or 0


def list_all(db: Session, offset: int = 0, limit: int = 20) -> list[Kategori]:
    return list(db.scalars(select(Kategori).order_by(Kategori.id).offset(offset).limit(limit)))


def get_by_id(db: Session, kategori_id: int) -> Kategori | None:
    return db.get(Kategori, kategori_id)


def create(db: Session, data: dict) -> Kategori:
    kategori = Kategori(**data)
    db.add(kategori)
    db.flush()
    return kategori


def update(db: Session, kategori: Kategori, data: dict) -> Kategori:
    for key, value in data.items():
        setattr(kategori, key, value)
    db.flush()
    return kategori


def delete(db: Session, kategori: Kategori) -> None:
    db.delete(kategori)
    db.flush()
