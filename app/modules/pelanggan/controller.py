from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.modules.admin.model import Admin
from app.modules.pelanggan.schema import PelangganResponse
from app.modules.pelanggan.service import get_pelanggan, list_pelanggan
from app.shared.pagination import calculate_offset, pagination_meta
from app.shared.response import success_response

router = APIRouter(prefix="/pelanggan", tags=["Pelanggan"])


@router.get("")
def get_pelanggan_list(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    items, total = list_pelanggan(db, calculate_offset(page, limit), limit, search)
    data = [PelangganResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar pelanggan", data, pagination_meta(page, limit, total))


@router.get("/{pelanggan_id}")
def get_pelanggan_detail(
    pelanggan_id: int,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    pelanggan = get_pelanggan(db, pelanggan_id)
    return success_response(
        "Detail pelanggan",
        PelangganResponse.model_validate(pelanggan).model_dump(mode="json"),
    )
