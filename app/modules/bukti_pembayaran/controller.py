from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.modules.admin.model import Admin
from app.modules.bukti_pembayaran.schema import (
    BuktiPembayaranResponse,
    BuktiPembayaranUploadResponse,
)
from app.modules.bukti_pembayaran.service import (
    delete_bukti,
    list_bukti_by_pesanan,
    upload_bukti_tanpa_login,
)
from app.shared.enums import StatusPembayaran
from app.shared.file_validator import validate_upload_file
from app.shared.response import success_response

router = APIRouter(prefix="/bukti-pembayaran", tags=["Bukti Pembayaran"])


@router.post("/upload-tanpa-login")
async def upload_bukti_endpoint(
    kode_pesanan: str = Form(...),
    no_telepon: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_database),
):
    validate_upload_file(file)
    content = await file.read()
    upload_bukti_tanpa_login(
        db,
        kode_pesanan=kode_pesanan,
        no_telepon=no_telepon,
        original_filename=file.filename or "bukti.jpg",
        content=content,
    )
    response = BuktiPembayaranUploadResponse(
        message="Bukti pembayaran berhasil diunggah",
        kode_pesanan=kode_pesanan,
        status_pembayaran=StatusPembayaran.MENUNGGU_VERIFIKASI.value,
    )
    return success_response(response.message, response.model_dump(mode="json"))


@router.get("/{pesanan_id}")
def get_bukti_by_pesanan(
    pesanan_id: int,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    items = list_bukti_by_pesanan(db, pesanan_id)
    data = [BuktiPembayaranResponse.model_validate(item).model_dump(mode="json") for item in items]
    return success_response("Daftar bukti pembayaran", data)


@router.delete("/{bukti_id}")
def delete_bukti_endpoint(
    bukti_id: int,
    db: Session = Depends(get_database),
    _: Admin = Depends(get_current_admin),
):
    delete_bukti(db, bukti_id)
    return success_response("Bukti pembayaran berhasil dihapus")
