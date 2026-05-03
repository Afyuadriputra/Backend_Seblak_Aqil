from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class KategoriBase(BaseModel):
    nama_kategori: str = Field(..., min_length=1, max_length=100)
    deskripsi: str | None = None


class KategoriCreate(KategoriBase):
    pass


class KategoriUpdate(BaseModel):
    nama_kategori: str | None = Field(default=None, min_length=1, max_length=100)
    deskripsi: str | None = None


class KategoriResponse(KategoriBase):
    id: int
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
