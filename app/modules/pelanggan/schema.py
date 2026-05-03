from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PelangganBase(BaseModel):
    nama_pelanggan: str = Field(..., min_length=1, max_length=100)
    no_telepon: str = Field(..., min_length=8, max_length=20)
    alamat: str = Field(..., min_length=1)


class PelangganCreate(PelangganBase):
    pass


class PelangganUpdate(BaseModel):
    nama_pelanggan: str | None = Field(default=None, min_length=1, max_length=100)
    no_telepon: str | None = Field(default=None, min_length=8, max_length=20)
    alamat: str | None = Field(default=None, min_length=1)


class PelangganResponse(PelangganBase):
    id: int
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
