from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.modules.admin.model import Admin
from app.modules.audit_log.schema import AuditLogResponse
from app.modules.audit_log.service import list_audit_logs
from app.shared.pagination import calculate_offset, pagination_meta
from app.shared.response import success_response

router = APIRouter(prefix="/audit-log", tags=["Audit Log"])


@router.get("")
def get_audit_logs(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    admin_id: int | None = Query(default=None, gt=0),
    aksi: str | None = Query(default=None),
    entity: str | None = Query(default=None),
    entity_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    items, total = list_audit_logs(
        db,
        calculate_offset(page, limit),
        limit,
        admin_id=admin_id,
        aksi=aksi,
        entity=entity,
        entity_id=entity_id,
    )
    data = [AuditLogResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar audit log", data, pagination_meta(page, limit, total))
