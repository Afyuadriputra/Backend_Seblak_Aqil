from decimal import Decimal
from pathlib import Path

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.redis_client import delete_pattern
from app.modules.kategori.repository import get_by_id as get_kategori_by_id
from app.modules.produk import repository
from app.modules.produk.model import Produk
from app.modules.produk.schema import (
    ProdukCreate,
    ProdukStatusUpdate,
    ProdukStokUpdate,
    ProdukUpdate,
)
from app.shared.exceptions import BadRequestException, NotFoundException
from app.shared.file_validator import generate_safe_filename, validate_file_size

settings = get_settings()


def list_produk(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    public_only: bool = False,
    search: str | None = None,
    kategori_id: int | None = None,
    status_tersedia: bool | None = None,
    min_harga: Decimal | None = None,
    max_harga: Decimal | None = None,
) -> tuple[list[Produk], int]:
    return (
        repository.list_all(
            db,
            offset,
            limit,
            public_only,
            search,
            kategori_id,
            status_tersedia,
            min_harga,
            max_harga,
        ),
        repository.count_all(
            db,
            public_only,
            search,
            kategori_id,
            status_tersedia,
            min_harga,
            max_harga,
        ),
    )


def get_produk(db: Session, produk_id: int, public_only: bool = False) -> Produk:
    produk = repository.get_by_id(db, produk_id, public_only)
    if produk is None:
        raise NotFoundException("Produk tidak ditemukan")
    return produk


def validate_kategori_exists(db: Session, kategori_id: int) -> None:
    if get_kategori_by_id(db, kategori_id) is None:
        raise BadRequestException("Kategori tidak ditemukan")


def create_produk(db: Session, payload: ProdukCreate) -> Produk:
    validate_kategori_exists(db, payload.kategori_id)
    produk = repository.create(db, payload.model_dump())
    db.commit()
    invalidate_produk_cache()
    db.refresh(produk)
    return produk


def update_produk(db: Session, produk_id: int, payload: ProdukUpdate) -> Produk:
    produk = get_produk(db, produk_id)
    data = payload.model_dump(exclude_unset=True)
    if "kategori_id" in data:
        validate_kategori_exists(db, data["kategori_id"])
    produk = repository.update(db, produk, data)
    db.commit()
    invalidate_produk_cache()
    db.refresh(produk)
    return produk


def update_produk_status(db: Session, produk_id: int, payload: ProdukStatusUpdate) -> Produk:
    produk = get_produk(db, produk_id)
    produk = repository.update(db, produk, {"status_tersedia": payload.status_tersedia})
    db.commit()
    invalidate_produk_cache()
    db.refresh(produk)
    return produk


def update_produk_stok(db: Session, produk_id: int, payload: ProdukStokUpdate) -> Produk:
    produk = get_produk(db, produk_id)
    produk = repository.update(db, produk, {"stok": payload.stok})
    db.commit()
    invalidate_produk_cache()
    db.refresh(produk)
    return produk


def update_produk_gambar(
    db: Session,
    produk_id: int,
    original_filename: str,
    content: bytes,
) -> Produk:
    produk = get_produk(db, produk_id)
    validate_file_size(len(content))

    safe_filename = generate_safe_filename(original_filename)
    upload_dir = settings.upload_path / "produk"
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / safe_filename
    old_path = Path(produk.gambar) if produk.gambar else None

    try:
        path.write_bytes(content)
        produk.gambar = str(path)
        db.commit()
        invalidate_produk_cache()
        db.refresh(produk)
        if old_path and old_path.exists() and old_path != path:
            old_path.unlink()
        return produk
    except Exception:
        db.rollback()
        if path.exists():
            path.unlink()
        raise


def delete_produk(db: Session, produk_id: int) -> None:
    produk = get_produk(db, produk_id)
    try:
        repository.delete(db, produk)
        db.commit()
        invalidate_produk_cache()
    except IntegrityError as exc:
        db.rollback()
        raise BadRequestException("Produk masih digunakan data lain") from exc


def invalidate_produk_cache() -> None:
    delete_pattern("produk:public:*")
    delete_pattern("dashboard:*")
