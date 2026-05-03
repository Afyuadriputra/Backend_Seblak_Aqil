from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings
from app.shared.exceptions import BadRequestException

settings = get_settings()

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


def validate_upload_file(file: UploadFile) -> None:
    validate_file_extension(file.filename)
    validate_file_mime_type(file.content_type)


def validate_file_extension(filename: str | None) -> None:
    if not filename:
        raise BadRequestException("Nama file tidak valid")

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise BadRequestException("Tipe file tidak diizinkan. Gunakan jpg, jpeg, png, atau webp.")


def validate_file_mime_type(content_type: str | None) -> None:
    if content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise BadRequestException("MIME type file tidak valid")


def validate_file_size(file_size: int) -> None:
    if file_size > settings.max_upload_size_bytes:
        raise BadRequestException(f"Ukuran file maksimal {settings.max_upload_size_mb} MB")


def generate_safe_filename(original_filename: str) -> str:
    extension = Path(original_filename).suffix.lower()
    return f"{uuid4().hex}{extension}"
