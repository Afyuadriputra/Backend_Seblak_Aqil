from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.core.redis_client import get_json_cache, set_json_cache
from app.modules.admin.model import Admin
from app.modules.metode_pembayaran.schema import (
    MetodePembayaranCreate,
    MetodePembayaranResponse,
    MetodePembayaranStatusUpdate,
    MetodePembayaranUpdate,
)
from app.modules.metode_pembayaran.service import (
    create_metode,
    delete_metode,
    get_metode,
    list_metode,
    list_metode_aktif,
    update_gambar_qr,
    update_metode,
    update_status,
)
from app.shared.file_validator import validate_upload_content, validate_upload_file
from app.shared.pagination import calculate_offset, pagination_meta
from app.shared.response import success_response

router = APIRouter(prefix="/metode-pembayaran", tags=["Metode Pembayaran"])


@router.get("")
def get_metode_list(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    items, total = list_metode(db, calculate_offset(page, limit), limit)
    data = [MetodePembayaranResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar metode pembayaran", data, pagination_meta(page, limit, total))


@router.get("/aktif")
def get_metode_aktif(db: Session = Depends(get_database)):
    cache_key = "metode-pembayaran:aktif"
    cached = get_json_cache(cache_key)
    if cached is not None:
        return success_response("Daftar metode pembayaran aktif", cached)

    items = list_metode_aktif(db)
    data = [MetodePembayaranResponse.model_validate(item).model_dump(mode="json") for item in items]
    set_json_cache(cache_key, data, 300)
    return success_response("Daftar metode pembayaran aktif", data)


@router.get("/{metode_id}")
def get_metode_detail(
    metode_id: int,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    metode = get_metode(db, metode_id)
    return success_response(
        "Detail metode pembayaran",
        MetodePembayaranResponse.model_validate(metode).model_dump(mode="json"),
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_metode_endpoint(
    payload: MetodePembayaranCreate,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    metode = create_metode(db, payload)
    return success_response(
        "Metode pembayaran berhasil dibuat",
        MetodePembayaranResponse.model_validate(metode).model_dump(mode="json"),
    )


@router.put("/{metode_id}")
def update_metode_endpoint(
    metode_id: int,
    payload: MetodePembayaranUpdate,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    metode = update_metode(db, metode_id, payload)
    return success_response(
        "Metode pembayaran berhasil diperbarui",
        MetodePembayaranResponse.model_validate(metode).model_dump(mode="json"),
    )


@router.patch("/{metode_id}/status")
def update_status_endpoint(
    metode_id: int,
    payload: MetodePembayaranStatusUpdate,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    metode = update_status(db, metode_id, payload)
    return success_response(
        "Status metode pembayaran berhasil diperbarui",
        MetodePembayaranResponse.model_validate(metode).model_dump(mode="json"),
    )


@router.patch("/{metode_id}/gambar-qr")
async def update_gambar_qr_endpoint(
    metode_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    validate_upload_file(file)
    content = await file.read()
    validate_upload_content(content, file.content_type)
    metode = update_gambar_qr(
        db,
        metode_id,
        original_filename=file.filename or "qris.jpg",
        content=content,
    )
    return success_response(
        "Gambar QR berhasil diperbarui",
        MetodePembayaranResponse.model_validate(metode).model_dump(mode="json"),
    )


@router.delete("/{metode_id}")
def delete_metode_endpoint(
    metode_id: int,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    delete_metode(db, metode_id)
    return success_response("Metode pembayaran berhasil dihapus")
