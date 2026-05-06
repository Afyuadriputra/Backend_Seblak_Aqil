from datetime import datetime

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.core.middleware import limiter
from app.modules.admin.model import Admin
from app.modules.pesanan.schema import (
    PesananCreate,
    PesananLacakRequest,
    PesananResponse,
    PesananRingkasResponse,
    PesananStatusPembayaranUpdate,
    PesananStatusPesananUpdate,
)
from app.modules.pesanan.service import (
    create_pesanan,
    get_pesanan,
    lacak_pesanan,
    list_pesanan,
    update_status_pembayaran,
    update_status_pesanan,
)
from app.shared.enums import StatusPembayaran, StatusPesanan
from app.shared.pagination import calculate_offset, pagination_meta
from app.shared.response import success_response

router = APIRouter(prefix="/pesanan", tags=["Pesanan"])


@router.post("", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_pesanan_endpoint(
    request: Request,
    payload: PesananCreate,
    db: Session = Depends(get_database),
):
    pesanan = create_pesanan(db, payload)
    return success_response(
        "Pesanan berhasil dibuat",
        PesananRingkasResponse.model_validate(pesanan).model_dump(mode="json"),
    )


@router.post("/lacak")
@limiter.limit("10/minute")
def lacak_pesanan_endpoint(
    request: Request,
    payload: PesananLacakRequest,
    db: Session = Depends(get_database),
):
    result = lacak_pesanan(db, payload)
    return success_response("Status pesanan", result.model_dump(mode="json"))


@router.get("")
def get_pesanan_list(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    status_pembayaran: StatusPembayaran | None = Query(default=None),
    status_pesanan: StatusPesanan | None = Query(default=None),
    kode_pesanan: str | None = Query(default=None),
    no_telepon: str | None = Query(default=None),
    tanggal_dari: datetime | None = Query(default=None),
    tanggal_sampai: datetime | None = Query(default=None),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    items, total = list_pesanan(
        db,
        calculate_offset(page, limit),
        limit,
        status_pembayaran,
        status_pesanan,
        kode_pesanan,
        no_telepon,
        tanggal_dari,
        tanggal_sampai,
    )
    data = [PesananResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar pesanan", data, pagination_meta(page, limit, total))


@router.get("/{pesanan_id}")
def get_pesanan_detail(
    pesanan_id: int,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    pesanan = get_pesanan(db, pesanan_id)
    return success_response(
        "Detail pesanan",
        PesananResponse.model_validate(pesanan).model_dump(mode="json"),
    )


@router.patch("/{pesanan_id}/status-pembayaran")
def update_status_pembayaran_endpoint(
    pesanan_id: int,
    payload: PesananStatusPembayaranUpdate,
    db: Session = Depends(get_database),
    current_admin: Admin = Depends(get_current_admin),
):
    pesanan = update_status_pembayaran(db, pesanan_id, payload, current_admin)
    return success_response(
        "Status pembayaran berhasil diperbarui",
        PesananResponse.model_validate(pesanan).model_dump(mode="json"),
    )


@router.patch("/{pesanan_id}/status-pesanan")
def update_status_pesanan_endpoint(
    pesanan_id: int,
    payload: PesananStatusPesananUpdate,
    db: Session = Depends(get_database),
    current_admin: Admin = Depends(get_current_admin),
):
    pesanan = update_status_pesanan(db, pesanan_id, payload, current_admin)
    return success_response(
        "Status pesanan berhasil diperbarui",
        PesananResponse.model_validate(pesanan).model_dump(mode="json"),
    )
