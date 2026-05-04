from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PesananTimelineResponse(BaseModel):
    id: int
    pesanan_id: int
    tipe_event: str
    status: str
    judul: str
    deskripsi: str
    waktu: datetime
    actor_type: str
    admin_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
