from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AdminBase(BaseModel):
    nama_admin: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=100)


class AdminCreate(AdminBase):
    kata_sandi: str = Field(..., min_length=8, max_length=128)


class AdminUpdate(BaseModel):
    nama_admin: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=3, max_length=100)


class AdminPasswordUpdate(BaseModel):
    kata_sandi_lama: str = Field(..., min_length=1)
    kata_sandi_baru: str = Field(..., min_length=8, max_length=128)


class AdminResponse(AdminBase):
    id: int
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
