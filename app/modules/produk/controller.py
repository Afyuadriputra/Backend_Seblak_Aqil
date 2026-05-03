from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.modules.admin.model import Admin
from app.modules.produk.schema import (
    ProdukCreate,
    ProdukResponse,
    ProdukStatusUpdate,
    ProdukStokUpdate,
    ProdukUpdate,
)
from app.modules.produk.service import (
    create_produk,
    delete_produk,
    get_produk,
    list_produk,
    update_produk,
    update_produk_status,
    update_produk_stok,
)
from app.shared.pagination import calculate_offset, pagination_meta
from app.shared.response import success_response

router = APIRouter(prefix="/produk", tags=["Produk"])


@router.get("")
def get_produk_list(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    kategori_id: int | None = Query(default=None, gt=0),
    min_harga: Decimal | None = Query(default=None, ge=0),
    max_harga: Decimal | None = Query(default=None, ge=0),
    db: Session = Depends(get_database),
):
    items, total = list_produk(
        db,
        calculate_offset(page, limit),
        limit,
        public_only=True,
        search=search,
        kategori_id=kategori_id,
        min_harga=min_harga,
        max_harga=max_harga,
    )
    data = [ProdukResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar produk", data, pagination_meta(page, limit, total))


@router.get("/admin/semua")
def get_produk_admin_list(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    kategori_id: int | None = Query(default=None, gt=0),
    status_tersedia: bool | None = Query(default=None),
    min_harga: Decimal | None = Query(default=None, ge=0),
    max_harga: Decimal | None = Query(default=None, ge=0),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    items, total = list_produk(
        db,
        calculate_offset(page, limit),
        limit,
        search=search,
        kategori_id=kategori_id,
        status_tersedia=status_tersedia,
        min_harga=min_harga,
        max_harga=max_harga,
    )
    data = [ProdukResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar produk admin", data, pagination_meta(page, limit, total))


@router.get("/admin/{produk_id}")
def get_produk_admin_detail(
    produk_id: int,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    produk = get_produk(db, produk_id)
    return success_response(
        "Detail produk admin",
        ProdukResponse.model_validate(produk).model_dump(mode="json"),
    )


@router.get("/{produk_id}")
def get_produk_detail(
    produk_id: int,
    db: Session = Depends(get_database),
):
    produk = get_produk(db, produk_id, public_only=True)
    return success_response(
        "Detail produk",
        ProdukResponse.model_validate(produk).model_dump(mode="json"),
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_produk_endpoint(
    payload: ProdukCreate,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    produk = create_produk(db, payload)
    return success_response(
        "Produk berhasil dibuat",
        ProdukResponse.model_validate(produk).model_dump(mode="json"),
    )


@router.put("/{produk_id}")
def update_produk_endpoint(
    produk_id: int,
    payload: ProdukUpdate,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    produk = update_produk(db, produk_id, payload)
    return success_response(
        "Produk berhasil diperbarui",
        ProdukResponse.model_validate(produk).model_dump(mode="json"),
    )


@router.patch("/{produk_id}/status")
def update_produk_status_endpoint(
    produk_id: int,
    payload: ProdukStatusUpdate,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    produk = update_produk_status(db, produk_id, payload)
    return success_response(
        "Status produk berhasil diperbarui",
        ProdukResponse.model_validate(produk).model_dump(mode="json"),
    )


@router.patch("/{produk_id}/stok")
def update_produk_stok_endpoint(
    produk_id: int,
    payload: ProdukStokUpdate,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    produk = update_produk_stok(db, produk_id, payload)
    return success_response(
        "Stok produk berhasil diperbarui",
        ProdukResponse.model_validate(produk).model_dump(mode="json"),
    )


@router.delete("/{produk_id}")
def delete_produk_endpoint(
    produk_id: int,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    delete_produk(db, produk_id)
    return success_response("Produk berhasil dihapus")
