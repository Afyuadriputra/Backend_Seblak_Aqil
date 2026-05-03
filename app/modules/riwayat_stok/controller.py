from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.modules.admin.model import Admin
from app.modules.riwayat_stok.schema import RiwayatStokRequest, RiwayatStokResponse
from app.modules.riwayat_stok.service import create_riwayat_stok, list_riwayat
from app.shared.enums import JenisPerubahanStok
from app.shared.pagination import calculate_offset, pagination_meta
from app.shared.response import success_response

router = APIRouter(prefix="/riwayat-stok", tags=["Riwayat Stok"])


@router.get("")
def get_riwayat_list(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    produk_id: int | None = Query(default=None, gt=0),
    admin_id: int | None = Query(default=None, gt=0),
    jenis_perubahan: JenisPerubahanStok | None = Query(default=None),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    items, total = list_riwayat(
        db,
        calculate_offset(page, limit),
        limit,
        produk_id=produk_id,
        admin_id=admin_id,
        jenis_perubahan=jenis_perubahan,
    )
    data = [RiwayatStokResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar riwayat stok", data, pagination_meta(page, limit, total))


@router.get("/produk/{produk_id}")
def get_riwayat_produk(
    produk_id: int,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    admin_id: int | None = Query(default=None, gt=0),
    jenis_perubahan: JenisPerubahanStok | None = Query(default=None),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    items, total = list_riwayat(
        db,
        calculate_offset(page, limit),
        limit,
        produk_id=produk_id,
        admin_id=admin_id,
        jenis_perubahan=jenis_perubahan,
    )
    data = [RiwayatStokResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar riwayat stok produk", data, pagination_meta(page, limit, total))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_riwayat_endpoint(
    payload: RiwayatStokRequest,
    db: Session = Depends(get_database),
    current_admin: Admin = Depends(get_current_admin),
):
    riwayat = create_riwayat_stok(db, payload, current_admin)
    return success_response(
        "Riwayat stok berhasil dibuat",
        RiwayatStokResponse.model_validate(riwayat).model_dump(mode="json"),
    )
