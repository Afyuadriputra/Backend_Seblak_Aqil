from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.modules.pelanggan.model import Pelanggan
from app.modules.pesanan.model import Pesanan
from app.modules.pesanan_timeline.model import PesananTimeline
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


def list_aktivitas_pesanan_terbaru(
    db: Session,
    limit: int = 10,
    tanggal_dari: datetime | None = None,
    tanggal_sampai: datetime | None = None,
) -> list[dict]:
    stmt = (
        select(
            PesananTimeline.id,
            PesananTimeline.pesanan_id,
            Pesanan.kode_pesanan,
            Pesanan.nama_pelanggan,
            PesananTimeline.tipe_event,
            PesananTimeline.status,
            PesananTimeline.judul,
            PesananTimeline.deskripsi,
            PesananTimeline.waktu,
            PesananTimeline.actor_type,
            PesananTimeline.admin_id,
        )
        .join(Pesanan, Pesanan.id == PesananTimeline.pesanan_id)
        .order_by(PesananTimeline.waktu.desc(), PesananTimeline.id.desc())
        .limit(limit)
    )
    stmt = apply_timeline_date_filter(stmt, tanggal_dari, tanggal_sampai)
    return [dict(row) for row in db.execute(stmt).mappings()]


def apply_date_filter(stmt, tanggal_dari: datetime | None, tanggal_sampai: datetime | None):
    if tanggal_dari is not None:
        stmt = stmt.where(Pesanan.tanggal_pesanan >= tanggal_dari)
    if tanggal_sampai is not None:
        stmt = stmt.where(Pesanan.tanggal_pesanan <= tanggal_sampai)
    return stmt


def apply_timeline_date_filter(
    stmt,
    tanggal_dari: datetime | None,
    tanggal_sampai: datetime | None,
):
    if tanggal_dari is not None:
        stmt = stmt.where(PesananTimeline.waktu >= tanggal_dari)
    if tanggal_sampai is not None:
        stmt = stmt.where(PesananTimeline.waktu <= tanggal_sampai)
    return stmt
