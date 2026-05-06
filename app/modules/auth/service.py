from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.modules.audit_log.service import record_audit
from app.modules.auth.repository import get_admin_by_email
from app.modules.auth.schema import LoginRequest, TokenResponse
from app.shared.exceptions import UnauthorizedException


def login(db: Session, payload: LoginRequest) -> TokenResponse:
    admin = get_admin_by_email(db, payload.email)

    if admin is None or not verify_password(payload.kata_sandi, admin.kata_sandi):
        record_audit(
            db,
            aksi="login_admin_gagal",
            entity="admin",
            deskripsi="Login admin gagal",
            metadata={"email": payload.email},
        )
        db.commit()
        raise UnauthorizedException("Email atau kata sandi salah")
    if not admin.is_active:
        record_audit(
            db,
            aksi="login_admin_gagal",
            entity="admin",
            entity_id=admin.id,
            admin_id=admin.id,
            deskripsi="Login admin gagal karena akun tidak aktif",
        )
        db.commit()
        raise UnauthorizedException("Email atau kata sandi salah")

    token = create_access_token(
        subject=str(admin.id),
        additional_claims={
            "admin_id": admin.id,
            "email": admin.email,
            "role": admin.role,
        },
    )
    record_audit(
        db,
        aksi="login_admin",
        entity="admin",
        entity_id=admin.id,
        admin_id=admin.id,
        deskripsi="Admin berhasil login",
    )
    db.commit()

    return TokenResponse(access_token=token)
