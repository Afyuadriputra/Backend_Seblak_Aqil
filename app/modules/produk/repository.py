from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.orm import Session, selectinload

from app.modules.produk.model import Produk


def count_all(
    db: Session,
    public_only: bool = False,
    search: str | None = None,
    kategori_id: int | None = None,
    status_tersedia: bool | None = None,
    min_harga: Decimal | None = None,
    max_harga: Decimal | None = None,
) -> int:
    stmt = select(func.count()).select_from(Produk)
    stmt = apply_filters(
        stmt,
        public_only,
        search,
        kategori_id,
        status_tersedia,
        min_harga,
        max_harga,
    )
    return db.scalar(stmt) or 0


def list_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    public_only: bool = False,
    search: str | None = None,
    kategori_id: int | None = None,
    status_tersedia: bool | None = None,
    min_harga: Decimal | None = None,
    max_harga: Decimal | None = None,
) -> list[Produk]:
    stmt = select(Produk).options(selectinload(Produk.kategori)).order_by(Produk.id)
    stmt = apply_filters(
        stmt,
        public_only,
        search,
        kategori_id,
        status_tersedia,
        min_harga,
        max_harga,
    )
    return list(db.scalars(stmt.offset(offset).limit(limit)))


def get_by_id(db: Session, produk_id: int, public_only: bool = False) -> Produk | None:
    stmt = select(Produk).options(selectinload(Produk.kategori)).where(Produk.id == produk_id)
    if public_only:
        stmt = stmt.where(Produk.status_tersedia.is_(True))
    return db.scalar(stmt)


def get_many_by_ids(db: Session, produk_ids: list[int]) -> list[Produk]:
    if not produk_ids:
        return []
    return list(db.scalars(select(Produk).where(Produk.id.in_(produk_ids))))


def decrease_stock_atomic(db: Session, produk_id: int, qty: int) -> bool:
    result = db.execute(
        sqlalchemy_update(Produk)
        .where(
            Produk.id == produk_id,
            Produk.stok >= qty,
            Produk.status_tersedia.is_(True),
        )
        .values(stok=Produk.stok - qty)
        .execution_options(synchronize_session=False)
    )
    return result.rowcount == 1


def create(db: Session, data: dict) -> Produk:
    produk = Produk(**data)
    db.add(produk)
    db.flush()
    return produk


def update(db: Session, produk: Produk, data: dict) -> Produk:
    for key, value in data.items():
        setattr(produk, key, value)
    db.flush()
    return produk


def delete(db: Session, produk: Produk) -> None:
    db.delete(produk)
    db.flush()


def apply_filters(
    stmt,
    public_only: bool,
    search: str | None,
    kategori_id: int | None,
    status_tersedia: bool | None,
    min_harga: Decimal | None,
    max_harga: Decimal | None,
):
    if public_only:
        stmt = stmt.where(Produk.status_tersedia.is_(True))
    elif status_tersedia is not None:
        stmt = stmt.where(Produk.status_tersedia.is_(status_tersedia))
    if search:
        stmt = stmt.where(Produk.nama_produk.ilike(f"%{search}%"))
    if kategori_id is not None:
        stmt = stmt.where(Produk.kategori_id == kategori_id)
    if min_harga is not None:
        stmt = stmt.where(Produk.harga >= min_harga)
    if max_harga is not None:
        stmt = stmt.where(Produk.harga <= max_harga)
    return stmt
