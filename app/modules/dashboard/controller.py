from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.core.redis_client import get_json_cache, set_json_cache
from app.modules.admin.model import Admin
from app.modules.dashboard.service import (
    get_aktivitas_pesanan_terbaru,
    get_produk_stok_rendah,
    get_summary,
)
from app.shared.response import success_response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary(
    tanggal_dari: datetime | None = Query(default=None),
    tanggal_sampai: datetime | None = Query(default=None),
    stok_threshold: int = Query(default=5, ge=0),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    cache_key = (
        "dashboard:summary:"
        f"dari={tanggal_dari.isoformat() if tanggal_dari else ''}:"
        f"sampai={tanggal_sampai.isoformat() if tanggal_sampai else ''}:"
        f"stok={stok_threshold}"
    )
    cached = get_json_cache(cache_key)
    if cached is not None:
        return success_response("Ringkasan dashboard", cached)

    summary = get_summary(db, tanggal_dari, tanggal_sampai, stok_threshold)
    data = summary.model_dump(mode="json")
    set_json_cache(cache_key, data, 60)
    return success_response("Ringkasan dashboard", data)


@router.get("/produk-stok-rendah")
def produk_stok_rendah(
    threshold: int = Query(default=5, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    result = get_produk_stok_rendah(db, threshold, limit)
    return success_response("Produk stok rendah", result.model_dump(mode="json"))


@router.get("/aktivitas-pesanan-terbaru")
def aktivitas_pesanan_terbaru(
    limit: int = Query(default=10, ge=1, le=100),
    tanggal_dari: datetime | None = Query(default=None),
    tanggal_sampai: datetime | None = Query(default=None),
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    result = get_aktivitas_pesanan_terbaru(db, limit, tanggal_dari, tanggal_sampai)
    return success_response("Aktivitas pesanan terbaru", result.model_dump(mode="json"))
