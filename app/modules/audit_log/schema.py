from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditLogResponse(BaseModel):
    id: int
    admin_id: int | None = None
    aksi: str
    entity: str
    entity_id: int | None = None
    deskripsi: str | None = None
    metadata_json: str | None = None
    dibuat_pada: datetime | None = None
    diperbarui_pada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AuditLogFilter(BaseModel):
    admin_id: int | None = Field(default=None, gt=0)
    aksi: str | None = None
    entity: str | None = None
    entity_id: int | None = Field(default=None, gt=0)
