from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BuktiPembayaranUploadRequest(BaseModel):
    kode_pesanan: str = Field(..., min_length=1, max_length=50)
    no_telepon: str = Field(..., min_length=8, max_length=20)


class BuktiPembayaranCreate(BaseModel):
    pesanan_id: int = Field(..., gt=0)
    nama_file: str = Field(..., min_length=1, max_length=255)
    path_file: str = Field(..., min_length=1, max_length=255)


class BuktiPembayaranResponse(BuktiPembayaranCreate):
    id: int
    diunggah_pada: datetime
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class BuktiPembayaranUploadResponse(BaseModel):
    message: str
    kode_pesanan: str
    status_pembayaran: str
