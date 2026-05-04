from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.modules.produk.schema import ProdukResponse


class DashboardPesananTimelineItemResponse(BaseModel):
    id: int
    pesanan_id: int
    kode_pesanan: str
    nama_pelanggan: str
    tipe_event: str
    status: str
    judul: str
    deskripsi: str
    waktu: datetime
    actor_type: str
    admin_id: int | None = None


class DashboardSummaryResponse(BaseModel):
    total_produk: int
    total_pelanggan: int
    total_pesanan: int
    pesanan_selesai: int
    pembayaran_menunggu_verifikasi: int
    produk_stok_rendah: int
    total_omzet: Decimal
    aktivitas_pesanan_terbaru: list[DashboardPesananTimelineItemResponse] = []
    tanggal_dari: datetime | None = None
    tanggal_sampai: datetime | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_produk": 12,
                "total_pelanggan": 30,
                "total_pesanan": 45,
                "pesanan_selesai": 20,
                "pembayaran_menunggu_verifikasi": 5,
                "produk_stok_rendah": 3,
                "total_omzet": "350000.00",
                "aktivitas_pesanan_terbaru": [],
                "tanggal_dari": "2026-05-01T00:00:00",
                "tanggal_sampai": "2026-05-31T23:59:59",
            }
        }
    )


class ProdukStokRendahResponse(BaseModel):
    threshold: int
    items: list[ProdukResponse]


class DashboardPesananTimelineResponse(BaseModel):
    items: list[DashboardPesananTimelineItemResponse]
