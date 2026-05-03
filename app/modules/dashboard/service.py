from datetime import datetime

from sqlalchemy.orm import Session

from app.modules.dashboard import repository
from app.modules.dashboard.schema import DashboardSummaryResponse, ProdukStokRendahResponse
from app.modules.produk.schema import ProdukResponse


def get_summary(
    db: Session,
    tanggal_dari: datetime | None = None,
    tanggal_sampai: datetime | None = None,
    stok_threshold: int = 5,
) -> DashboardSummaryResponse:
    return DashboardSummaryResponse(
        total_produk=repository.count_produk(db),
        total_pelanggan=repository.count_pelanggan(db),
        total_pesanan=repository.count_pesanan(db, tanggal_dari, tanggal_sampai),
        pesanan_selesai=repository.count_pesanan_selesai(db, tanggal_dari, tanggal_sampai),
        pembayaran_menunggu_verifikasi=repository.count_pembayaran_menunggu(
            db,
            tanggal_dari,
            tanggal_sampai,
        ),
        produk_stok_rendah=repository.count_produk_stok_rendah(db, stok_threshold),
        total_omzet=repository.sum_omzet(db, tanggal_dari, tanggal_sampai),
        tanggal_dari=tanggal_dari,
        tanggal_sampai=tanggal_sampai,
    )


def get_produk_stok_rendah(
    db: Session,
    threshold: int = 5,
    limit: int = 20,
) -> ProdukStokRendahResponse:
    items = repository.list_produk_stok_rendah(db, threshold, limit)
    return ProdukStokRendahResponse(
        threshold=threshold,
        items=[ProdukResponse.model_validate(item) for item in items],
    )
