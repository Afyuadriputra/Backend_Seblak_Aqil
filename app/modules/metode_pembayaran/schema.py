from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.shared.enums import TipeMetodePembayaran


class MetodePembayaranBase(BaseModel):
    nama_metode: str = Field(..., min_length=1, max_length=100)
    tipe_metode: TipeMetodePembayaran
    nama_bank: str | None = Field(default=None, max_length=100)
    nomor_rekening: str | None = Field(default=None, max_length=50)
    nama_pemilik_rekening: str | None = Field(default=None, max_length=100)
    gambar_qr: str | None = Field(default=None, max_length=255)
    status_aktif: bool = True

    @model_validator(mode="after")
    def validate_payment_fields(self):
        if self.tipe_metode == TipeMetodePembayaran.QRIS and not self.gambar_qr:
            raise ValueError("gambar_qr wajib diisi untuk metode QRIS")

        if self.tipe_metode == TipeMetodePembayaran.TRANSFER_BANK:
            if not self.nama_bank or not self.nomor_rekening or not self.nama_pemilik_rekening:
                raise ValueError("data rekening wajib diisi untuk metode transfer_bank")

        return self


class MetodePembayaranCreate(MetodePembayaranBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"nama_metode": "QRIS", "tipe_metode": "qris", "gambar_qr": "qris.png"},
                {
                    "nama_metode": "Transfer BCA",
                    "tipe_metode": "transfer_bank",
                    "nama_bank": "BCA",
                    "nomor_rekening": "1234567890",
                    "nama_pemilik_rekening": "Seblak Rika",
                },
            ]
        }
    )


class MetodePembayaranUpdate(BaseModel):
    nama_metode: str | None = Field(default=None, min_length=1, max_length=100)
    tipe_metode: TipeMetodePembayaran | None = None
    nama_bank: str | None = Field(default=None, max_length=100)
    nomor_rekening: str | None = Field(default=None, max_length=50)
    nama_pemilik_rekening: str | None = Field(default=None, max_length=100)
    gambar_qr: str | None = Field(default=None, max_length=255)
    status_aktif: bool | None = None


class MetodePembayaranStatusUpdate(BaseModel):
    status_aktif: bool


class MetodePembayaranResponse(MetodePembayaranBase):
    id: int
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
