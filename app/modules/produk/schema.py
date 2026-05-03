from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProdukBase(BaseModel):
    kategori_id: int = Field(..., gt=0)
    nama_produk: str = Field(..., min_length=1, max_length=150)
    deskripsi: str | None = None
    harga: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2)
    stok: int = Field(default=0, ge=0)
    gambar: str | None = Field(default=None, max_length=255)
    status_tersedia: bool = True


class ProdukCreate(ProdukBase):
    pass


class ProdukUpdate(BaseModel):
    kategori_id: int | None = Field(default=None, gt=0)
    nama_produk: str | None = Field(default=None, min_length=1, max_length=150)
    deskripsi: str | None = None
    harga: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    stok: int | None = Field(default=None, ge=0)
    gambar: str | None = Field(default=None, max_length=255)
    status_tersedia: bool | None = None


class ProdukStatusUpdate(BaseModel):
    status_tersedia: bool


class ProdukStokUpdate(BaseModel):
    stok: int = Field(..., ge=0)


class ProdukResponse(ProdukBase):
    id: int
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
