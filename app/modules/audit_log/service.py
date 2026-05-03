import json
from typing import Any

from sqlalchemy.orm import Session

from app.modules.audit_log import repository
from app.modules.audit_log.model import AuditLog


def record_audit(
    db: Session,
    aksi: str,
    entity: str,
    entity_id: int | None = None,
    admin_id: int | None = None,
    deskripsi: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> AuditLog:
    return repository.create(
        db,
        {
            "admin_id": admin_id,
            "aksi": aksi,
            "entity": entity,
            "entity_id": entity_id,
            "deskripsi": deskripsi,
            "metadata_json": json.dumps(metadata, default=str) if metadata else None,
        },
    )


def list_audit_logs(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    admin_id: int | None = None,
    aksi: str | None = None,
    entity: str | None = None,
    entity_id: int | None = None,
) -> tuple[list[AuditLog], int]:
    return (
        repository.list_all(db, offset, limit, admin_id, aksi, entity, entity_id),
        repository.count_all(db, admin_id, aksi, entity, entity_id),
    )
