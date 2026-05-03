from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.modules.pelanggan.model import Pelanggan


def count_all(db: Session, search: str | None = None) -> int:
    stmt = select(func.count()).select_from(Pelanggan)
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(Pelanggan.nama_pelanggan.ilike(pattern), Pelanggan.no_telepon.ilike(pattern))
        )
    return db.scalar(stmt) or 0


def list_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    search: str | None = None,
) -> list[Pelanggan]:
    stmt = select(Pelanggan).order_by(Pelanggan.id.desc())
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(Pelanggan.nama_pelanggan.ilike(pattern), Pelanggan.no_telepon.ilike(pattern))
        )
    return list(db.scalars(stmt.offset(offset).limit(limit)))


def get_by_id(db: Session, pelanggan_id: int) -> Pelanggan | None:
    return db.get(Pelanggan, pelanggan_id)


def create(db: Session, data: dict) -> Pelanggan:
    pelanggan = Pelanggan(**data)
    db.add(pelanggan)
    db.flush()
    return pelanggan
