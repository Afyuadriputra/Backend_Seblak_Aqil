from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.modules.pesanan.model import DetailPesanan, Pesanan


def count_all(
    db: Session,
    status_pembayaran: str | None = None,
    status_pesanan: str | None = None,
    kode_pesanan: str | None = None,
    no_telepon: str | None = None,
    tanggal_dari: datetime | None = None,
    tanggal_sampai: datetime | None = None,
) -> int:
    stmt = select(func.count()).select_from(Pesanan)
    stmt = apply_filters(
        stmt,
        status_pembayaran,
        status_pesanan,
        kode_pesanan,
        no_telepon,
        tanggal_dari,
        tanggal_sampai,
    )
    return db.scalar(stmt) or 0


def list_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    status_pembayaran: str | None = None,
    status_pesanan: str | None = None,
    kode_pesanan: str | None = None,
    no_telepon: str | None = None,
    tanggal_dari: datetime | None = None,
    tanggal_sampai: datetime | None = None,
) -> list[Pesanan]:
    stmt = (
        select(Pesanan)
        .options(
            selectinload(Pesanan.detail_pesanan),
            selectinload(Pesanan.metode_pembayaran),
            selectinload(Pesanan.bukti_pembayaran),
            selectinload(Pesanan.timeline),
        )
        .order_by(Pesanan.tanggal_pesanan.desc(), Pesanan.id.desc())
    )
    stmt = apply_filters(
        stmt,
        status_pembayaran,
        status_pesanan,
        kode_pesanan,
        no_telepon,
        tanggal_dari,
        tanggal_sampai,
    )
    return list(db.scalars(stmt.offset(offset).limit(limit)))


def get_by_id(db: Session, pesanan_id: int) -> Pesanan | None:
    return db.scalar(
        select(Pesanan)
        .options(
            selectinload(Pesanan.detail_pesanan),
            selectinload(Pesanan.metode_pembayaran),
            selectinload(Pesanan.bukti_pembayaran),
            selectinload(Pesanan.timeline),
        )
        .where(Pesanan.id == pesanan_id)
    )


def get_by_code_and_phone(db: Session, kode_pesanan: str, no_telepon: str) -> Pesanan | None:
    return db.scalar(
        select(Pesanan)
        .options(
            selectinload(Pesanan.detail_pesanan),
            selectinload(Pesanan.metode_pembayaran),
            selectinload(Pesanan.bukti_pembayaran),
            selectinload(Pesanan.timeline),
        )
        .where(
            Pesanan.kode_pesanan == kode_pesanan,
            Pesanan.no_telepon_pelanggan == no_telepon,
        )
    )


def get_by_code(db: Session, kode_pesanan: str) -> Pesanan | None:
    return db.scalar(select(Pesanan).where(Pesanan.kode_pesanan == kode_pesanan))


def create(db: Session, data: dict) -> Pesanan:
    pesanan = Pesanan(**data)
    db.add(pesanan)
    db.flush()
    return pesanan


def create_detail(db: Session, data: dict) -> DetailPesanan:
    detail = DetailPesanan(**data)
    db.add(detail)
    db.flush()
    return detail


def update(db: Session, pesanan: Pesanan, data: dict) -> Pesanan:
    for key, value in data.items():
        setattr(pesanan, key, value)
    db.flush()
    return pesanan


def apply_filters(
    stmt,
    status_pembayaran: str | None,
    status_pesanan: str | None,
    kode_pesanan: str | None,
    no_telepon: str | None,
    tanggal_dari: datetime | None,
    tanggal_sampai: datetime | None,
):
    if status_pembayaran:
        stmt = stmt.where(Pesanan.status_pembayaran == status_pembayaran)
    if status_pesanan:
        stmt = stmt.where(Pesanan.status_pesanan == status_pesanan)
    if kode_pesanan:
        stmt = stmt.where(Pesanan.kode_pesanan.ilike(f"%{kode_pesanan}%"))
    if no_telepon:
        stmt = stmt.where(Pesanan.no_telepon_pelanggan.ilike(f"%{no_telepon}%"))
    if tanggal_dari is not None:
        stmt = stmt.where(Pesanan.tanggal_pesanan >= tanggal_dari)
    if tanggal_sampai is not None:
        stmt = stmt.where(Pesanan.tanggal_pesanan <= tanggal_sampai)
    return stmt
