from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.modules.riwayat_stok.model import RiwayatStok


def count_all(
    db: Session,
    produk_id: int | None = None,
    admin_id: int | None = None,
    jenis_perubahan: str | None = None,
) -> int:
    stmt = select(func.count()).select_from(RiwayatStok)
    stmt = apply_filters(stmt, produk_id, admin_id, jenis_perubahan)
    return db.scalar(stmt) or 0


def list_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    produk_id: int | None = None,
    admin_id: int | None = None,
    jenis_perubahan: str | None = None,
) -> list[RiwayatStok]:
    stmt = (
        select(RiwayatStok)
        .options(selectinload(RiwayatStok.produk), selectinload(RiwayatStok.admin))
        .order_by(RiwayatStok.id.desc())
    )
    stmt = apply_filters(stmt, produk_id, admin_id, jenis_perubahan)
    return list(db.scalars(stmt.offset(offset).limit(limit)))


def create(db: Session, data: dict) -> RiwayatStok:
    riwayat = RiwayatStok(**data)
    db.add(riwayat)
    db.flush()
    return riwayat


def apply_filters(
    stmt,
    produk_id: int | None = None,
    admin_id: int | None = None,
    jenis_perubahan: str | None = None,
):
    if produk_id is not None:
        stmt = stmt.where(RiwayatStok.produk_id == produk_id)
    if admin_id is not None:
        stmt = stmt.where(RiwayatStok.admin_id == admin_id)
    if jenis_perubahan:
        stmt = stmt.where(RiwayatStok.jenis_perubahan == jenis_perubahan)
    return stmt
