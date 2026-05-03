from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.shared.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_database(db: Session = Depends(get_db)) -> Session:
    return db


def get_current_admin_token(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_access_token(token)

    if payload is None:
        raise UnauthorizedException("Token tidak valid atau sudah kedaluwarsa")

    return payload
