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
JPEG_SIGNATURES = (b"\xff\xd8\xff",)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
WEBP_RIFF = b"RIFF"
WEBP_SIGNATURE = b"WEBP"


def validate_upload_file(file: UploadFile) -> None:
    validate_file_extension(file.filename)
    validate_file_mime_type(file.content_type)


def validate_upload_content(content: bytes, content_type: str | None) -> None:
    validate_file_size(len(content))
    if content_type == "image/jpeg" and content.startswith(JPEG_SIGNATURES):
        return
    if content_type == "image/png" and content.startswith(PNG_SIGNATURE):
        return
    if (
        content_type == "image/webp"
        and len(content) >= 12
        and content.startswith(WEBP_RIFF)
        and content[8:12] == WEBP_SIGNATURE
    ):
        return
    raise BadRequestException("Konten file tidak sesuai dengan tipe gambar")


def validate_file_extension(filename: str | None) -> None:
    if not filename:
        raise BadRequestException("Nama file tidak valid")

    suffixes = [suffix.lower() for suffix in Path(filename).suffixes]
    extension = suffixes[-1] if suffixes else ""

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise BadRequestException("Tipe file tidak diizinkan. Gunakan jpg, jpeg, png, atau webp.")
    if len(suffixes) > 1 and any(suffix not in ALLOWED_IMAGE_EXTENSIONS for suffix in suffixes):
        raise BadRequestException("Nama file tidak valid")


def validate_file_mime_type(content_type: str | None) -> None:
    if content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise BadRequestException("MIME type file tidak valid")


def validate_file_size(file_size: int) -> None:
    if file_size <= 0:
        raise BadRequestException("File tidak boleh kosong")
    if file_size > settings.max_upload_size_bytes:
        raise BadRequestException(f"Ukuran file maksimal {settings.max_upload_size_mb} MB")


def generate_safe_filename(original_filename: str) -> str:
    extension = Path(original_filename).suffix.lower()
    return f"{uuid4().hex}{extension}"
