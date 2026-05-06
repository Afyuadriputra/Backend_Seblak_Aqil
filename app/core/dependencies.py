from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.admin.model import Admin
from app.shared.enums import AdminRole
from app.shared.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_database(db: Session = Depends(get_db)) -> Session:
    return db


def get_current_admin_token(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_access_token(token)

    if payload is None or not payload.get("sub"):
        raise UnauthorizedException("Token tidak valid atau sudah kedaluwarsa")

    return payload


def get_current_admin(
    token_payload: dict = Depends(get_current_admin_token),
    db: Session = Depends(get_database),
) -> Admin:
    admin_id = token_payload.get("admin_id") or token_payload.get("sub")

    if admin_id is None:
        raise UnauthorizedException("Token tidak valid")

    admin = db.scalar(select(Admin).where(Admin.id == int(admin_id)))

    if admin is None:
        raise UnauthorizedException("Admin tidak ditemukan")
    if not admin.is_active:
        raise UnauthorizedException("Token tidak valid atau sudah kedaluwarsa")

    return admin


def require_role(role: AdminRole | str):
    required_role = role.value if isinstance(role, AdminRole) else role

    def dependency(current_admin: Admin = Depends(get_current_admin)) -> Admin:
        if current_admin.role != required_role:
            raise UnauthorizedException("Token tidak valid atau sudah kedaluwarsa")
        return current_admin

    return dependency


def require_any_role(roles: list[AdminRole | str]):
    allowed_roles = {role.value if isinstance(role, AdminRole) else role for role in roles}

    def dependency(current_admin: Admin = Depends(get_current_admin)) -> Admin:
        if current_admin.role not in allowed_roles:
            raise UnauthorizedException("Token tidak valid atau sudah kedaluwarsa")
        return current_admin

    return dependency
