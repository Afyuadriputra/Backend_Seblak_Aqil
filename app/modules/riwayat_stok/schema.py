from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.shared.enums import JenisPerubahanStok


class RiwayatStokCreate(BaseModel):
    produk_id: int = Field(..., gt=0)
    admin_id: int = Field(..., gt=0)
    jenis_perubahan: JenisPerubahanStok
    stok_sebelum: int = Field(..., ge=0)
    jumlah_perubahan: int = Field(..., gt=0)
    stok_sesudah: int = Field(..., ge=0)
    keterangan: str | None = None

    @model_validator(mode="after")
    def validate_stock_result(self):
        if self.jenis_perubahan == JenisPerubahanStok.MASUK:
            expected = self.stok_sebelum + self.jumlah_perubahan
        elif self.jenis_perubahan == JenisPerubahanStok.KELUAR:
            expected = self.stok_sebelum - self.jumlah_perubahan
        else:
            return self

        if self.stok_sesudah != expected:
            raise ValueError("stok_sesudah tidak sesuai dengan jenis_perubahan")

        return self


class RiwayatStokResponse(RiwayatStokCreate):
    id: int
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class RiwayatStokRequest(BaseModel):
    produk_id: int = Field(..., gt=0)
    jenis_perubahan: JenisPerubahanStok
    jumlah_perubahan: int = Field(..., gt=0)
    stok_baru: int | None = Field(default=None, ge=0)
    keterangan: str | None = None

    @model_validator(mode="after")
    def validate_adjustment_target(self):
        if self.jenis_perubahan == JenisPerubahanStok.PENYESUAIAN and self.stok_baru is None:
            raise ValueError("stok_baru wajib diisi untuk penyesuaian")
        return self

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"produk_id": 1, "jenis_perubahan": "masuk", "jumlah_perubahan": 10},
                {"produk_id": 1, "jenis_perubahan": "keluar", "jumlah_perubahan": 2},
                {
                    "produk_id": 1,
                    "jenis_perubahan": "penyesuaian",
                    "jumlah_perubahan": 1,
                    "stok_baru": 20,
                },
            ]
        }
    )
