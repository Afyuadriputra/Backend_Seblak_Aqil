from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.modules.pelanggan.model import Pelanggan
from app.modules.pesanan.model import Pesanan
from app.modules.produk.model import Produk
from app.shared.enums import StatusPembayaran, StatusPesanan


def count_produk(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(Produk)) or 0


def count_pelanggan(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(Pelanggan)) or 0


def count_pesanan(
    db: Session,
    tanggal_dari: datetime | None = None,
    tanggal_sampai: datetime | None = None,
) -> int:
    stmt = select(func.count()).select_from(Pesanan)
    stmt = apply_date_filter(stmt, tanggal_dari, tanggal_sampai)
    return db.scalar(stmt) or 0


def count_pesanan_selesai(
    db: Session,
    tanggal_dari: datetime | None = None,
    tanggal_sampai: datetime | None = None,
) -> int:
    stmt = (
        select(func.count())
        .select_from(Pesanan)
        .where(Pesanan.status_pesanan == StatusPesanan.SELESAI.value)
    )
    stmt = apply_date_filter(stmt, tanggal_dari, tanggal_sampai)
    return db.scalar(stmt) or 0


def count_pembayaran_menunggu(
    db: Session,
    tanggal_dari: datetime | None = None,
    tanggal_sampai: datetime | None = None,
) -> int:
    stmt = (
        select(func.count())
        .select_from(Pesanan)
        .where(Pesanan.status_pembayaran == StatusPembayaran.MENUNGGU_VERIFIKASI.value)
    )
    stmt = apply_date_filter(stmt, tanggal_dari, tanggal_sampai)
    return db.scalar(stmt) or 0


def sum_omzet(
    db: Session,
    tanggal_dari: datetime | None = None,
    tanggal_sampai: datetime | None = None,
) -> Decimal:
    stmt = select(func.coalesce(func.sum(Pesanan.total_harga), 0)).where(
        Pesanan.status_pembayaran == StatusPembayaran.DITERIMA.value
    )
    stmt = apply_date_filter(stmt, tanggal_dari, tanggal_sampai)
    return db.scalar(stmt) or Decimal("0.00")


def count_produk_stok_rendah(db: Session, threshold: int) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(Produk)
            .where(Produk.stok <= threshold, Produk.status_tersedia.is_(True))
        )
        or 0
    )


def list_produk_stok_rendah(db: Session, threshold: int, limit: int = 20) -> list[Produk]:
    return list(
        db.scalars(
            select(Produk)
            .options(selectinload(Produk.kategori))
            .where(Produk.stok <= threshold, Produk.status_tersedia.is_(True))
            .order_by(Produk.stok.asc(), Produk.id.asc())
            .limit(limit)
        )
    )


def apply_date_filter(stmt, tanggal_dari: datetime | None, tanggal_sampai: datetime | None):
    if tanggal_dari is not None:
        stmt = stmt.where(Pesanan.tanggal_pesanan >= tanggal_dari)
    if tanggal_sampai is not None:
        stmt = stmt.where(Pesanan.tanggal_pesanan <= tanggal_sampai)
    return stmt
