from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.audit_log.model import AuditLog


def create(db: Session, data: dict) -> AuditLog:
    audit = AuditLog(**data)
    db.add(audit)
    db.flush()
    return audit


def count_all(
    db: Session,
    admin_id: int | None = None,
    aksi: str | None = None,
    entity: str | None = None,
    entity_id: int | None = None,
) -> int:
    stmt = select(func.count()).select_from(AuditLog)
    stmt = apply_filters(stmt, admin_id, aksi, entity, entity_id)
    return db.scalar(stmt) or 0


def list_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    admin_id: int | None = None,
    aksi: str | None = None,
    entity: str | None = None,
    entity_id: int | None = None,
) -> list[AuditLog]:
    stmt = select(AuditLog).order_by(AuditLog.id.desc())
    stmt = apply_filters(stmt, admin_id, aksi, entity, entity_id)
    return list(db.scalars(stmt.offset(offset).limit(limit)))


def apply_filters(stmt, admin_id, aksi, entity, entity_id):
    if admin_id is not None:
        stmt = stmt.where(AuditLog.admin_id == admin_id)
    if aksi:
        stmt = stmt.where(AuditLog.aksi == aksi)
    if entity:
        stmt = stmt.where(AuditLog.entity == entity)
    if entity_id is not None:
        stmt = stmt.where(AuditLog.entity_id == entity_id)
    return stmt
