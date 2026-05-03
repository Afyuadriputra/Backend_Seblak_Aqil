from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_database
from app.modules.admin.model import Admin
from app.modules.admin.schema import AdminResponse
from app.modules.auth.schema import LoginRequest, TokenResponse
from app.modules.auth.service import login
from app.shared.response import success_response

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login_admin(payload: LoginRequest, db: Session = Depends(get_database)):
    token: TokenResponse = login(db, payload)
    return success_response("Login berhasil", token.model_dump())


@router.get("/me")
def get_me(current_admin: Admin = Depends(get_current_admin)):
    return success_response(
        "Data admin aktif",
        AdminResponse.model_validate(current_admin).model_dump(mode="json"),
    )
