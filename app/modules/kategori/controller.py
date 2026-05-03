from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.modules.admin.model import Admin
from app.modules.kategori.schema import KategoriCreate, KategoriResponse, KategoriUpdate
from app.modules.kategori.service import (
    create_kategori,
    delete_kategori,
    get_kategori,
    list_kategori,
    update_kategori,
)
from app.shared.pagination import calculate_offset, pagination_meta
from app.shared.response import success_response

router = APIRouter(prefix="/kategori", tags=["Kategori"])


@router.get("")
def get_kategori_list(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_database),
):
    items, total = list_kategori(db, calculate_offset(page, limit), limit)
    data = [KategoriResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar kategori", data, pagination_meta(page, limit, total))


@router.get("/{kategori_id}")
def get_kategori_detail(kategori_id: int, db: Session = Depends(get_database)):
    kategori = get_kategori(db, kategori_id)
    return success_response(
        "Detail kategori",
        KategoriResponse.model_validate(kategori).model_dump(mode="json"),
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_kategori_endpoint(
    payload: KategoriCreate,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    kategori = create_kategori(db, payload)
    return success_response(
        "Kategori berhasil dibuat",
        KategoriResponse.model_validate(kategori).model_dump(mode="json"),
    )


@router.put("/{kategori_id}")
def update_kategori_endpoint(
    kategori_id: int,
    payload: KategoriUpdate,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    kategori = update_kategori(db, kategori_id, payload)
    return success_response(
        "Kategori berhasil diperbarui",
        KategoriResponse.model_validate(kategori).model_dump(mode="json"),
    )


@router.delete("/{kategori_id}")
def delete_kategori_endpoint(
    kategori_id: int,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    delete_kategori(db, kategori_id)
    return success_response("Kategori berhasil dihapus")
