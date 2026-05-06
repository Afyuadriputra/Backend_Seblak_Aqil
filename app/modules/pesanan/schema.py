from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.modules.pesanan_timeline.schema import (
    PesananTimelinePublicResponse,
    PesananTimelineResponse,
)
from app.shared.enums import StatusPembayaran, StatusPesanan


class PesananItemCreate(BaseModel):
    produk_id: int = Field(..., gt=0)
    jumlah: int = Field(..., gt=0, le=50)


class PesananCreate(BaseModel):
    nama_pelanggan: str = Field(..., min_length=1, max_length=100)
    no_telepon: str = Field(..., min_length=8, max_length=20)
    alamat: str = Field(..., min_length=1, max_length=500)
    metode_pembayaran_id: int = Field(..., gt=0)
    catatan: str | None = Field(default=None, max_length=500)
    items: list[PesananItemCreate] = Field(..., min_length=1, max_length=30)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nama_pelanggan": "Budi",
                "no_telepon": "08123456789",
                "alamat": "Jl. Mawar No. 10",
                "metode_pembayaran_id": 1,
                "catatan": "Pedas level 3",
                "items": [{"produk_id": 1, "jumlah": 2}],
            }
        }
    )


class PesananLacakRequest(BaseModel):
    kode_pesanan: str = Field(..., min_length=1, max_length=50)
    no_telepon: str = Field(..., min_length=8, max_length=20)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"kode_pesanan": "ORD-20260504-ABC12345", "no_telepon": "08123456789"}
        }
    )


class PesananStatusPembayaranUpdate(BaseModel):
    status_pembayaran: StatusPembayaran

    model_config = ConfigDict(json_schema_extra={"example": {"status_pembayaran": "diterima"}})


class PesananStatusPesananUpdate(BaseModel):
    status_pesanan: StatusPesanan

    model_config = ConfigDict(json_schema_extra={"example": {"status_pesanan": "diproses"}})


class DetailPesananResponse(BaseModel):
    id: int
    pesanan_id: int
    produk_id: int
    nama_produk: str
    harga_produk: Decimal
    jumlah: int
    subtotal: Decimal
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class PesananResponse(BaseModel):
    id: int
    pelanggan_id: int
    metode_pembayaran_id: int
    nama_metode_pembayaran: str | None = None
    tipe_metode_pembayaran: str | None = None
    kode_pesanan: str
    tanggal_pesanan: datetime
    total_harga: Decimal
    nama_pelanggan: str
    no_telepon_pelanggan: str
    alamat_pelanggan: str
    catatan: str | None = None
    status_pembayaran: StatusPembayaran
    status_pesanan: StatusPesanan
    detail_pesanan: list[DetailPesananResponse] = []
    timeline: list[PesananTimelineResponse] = []
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class PesananRingkasResponse(BaseModel):
    id: int
    kode_pesanan: str
    total_harga: Decimal
    status_pembayaran: StatusPembayaran
    status_pesanan: StatusPesanan

    model_config = ConfigDict(from_attributes=True)


class PesananLacakResponse(BaseModel):
    kode_pesanan: str
    nama_pelanggan: str
    metode_pembayaran: str
    status_pembayaran: StatusPembayaran
    status_pesanan: StatusPesanan
    total_harga: Decimal
    bukti_pembayaran_tersedia: bool
    timeline: list[PesananTimelinePublicResponse] = []


class DetailPesananCreate(BaseModel):
    pesanan_id: int = Field(..., gt=0)
    produk_id: int = Field(..., gt=0)
    nama_produk: str = Field(..., min_length=1, max_length=150)
    harga_produk: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2)
    jumlah: int = Field(..., gt=0)
    subtotal: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2)

    @model_validator(mode="after")
    def validate_subtotal(self):
        expected = self.harga_produk * self.jumlah
        if self.subtotal != expected:
            raise ValueError("subtotal harus sama dengan harga_produk dikali jumlah")
        return self
