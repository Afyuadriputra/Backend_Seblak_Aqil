from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.modules.admin.model import Admin
from app.modules.admin.schema import AdminPasswordUpdate, AdminResponse, AdminUpdate
from app.modules.admin.service import update_password, update_profile
from app.shared.response import success_response

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/me")
def get_profile(current_admin: Admin = Depends(get_current_admin)):
    return success_response(
        "Profil admin",
        AdminResponse.model_validate(current_admin).model_dump(mode="json"),
    )


@router.put("/me")
def update_admin_profile(
    payload: AdminUpdate,
    db: Session = Depends(get_database),
    current_admin: Admin = Depends(get_current_admin),
):
    admin = update_profile(db, current_admin, payload)
    return success_response(
        "Profil admin diperbarui",
        AdminResponse.model_validate(admin).model_dump(mode="json"),
    )


@router.put("/ubah-password")
def change_password(
    payload: AdminPasswordUpdate,
    db: Session = Depends(get_database),
    current_admin: Admin = Depends(get_current_admin),
):
    update_password(db, current_admin, payload)
    return success_response("Kata sandi berhasil diubah")
