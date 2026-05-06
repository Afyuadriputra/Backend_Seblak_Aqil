from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.redis_client import delete_pattern
from app.modules.kategori import repository
from app.modules.kategori.model import Kategori
from app.modules.kategori.schema import KategoriCreate, KategoriUpdate
from app.shared.exceptions import BadRequestException, NotFoundException


def list_kategori(db: Session, offset: int = 0, limit: int = 20) -> tuple[list[Kategori], int]:
    return repository.list_all(db, offset, limit), repository.count_all(db)


def get_kategori(db: Session, kategori_id: int) -> Kategori:
    kategori = repository.get_by_id(db, kategori_id)
    if kategori is None:
        raise NotFoundException("Kategori tidak ditemukan")
    return kategori


def create_kategori(db: Session, payload: KategoriCreate) -> Kategori:
    kategori = repository.create(db, payload.model_dump())
    db.commit()
    invalidate_kategori_cache()
    db.refresh(kategori)
    return kategori


def update_kategori(db: Session, kategori_id: int, payload: KategoriUpdate) -> Kategori:
    kategori = get_kategori(db, kategori_id)
    data = payload.model_dump(exclude_unset=True)
    kategori = repository.update(db, kategori, data)
    db.commit()
    invalidate_kategori_cache()
    db.refresh(kategori)
    return kategori


def delete_kategori(db: Session, kategori_id: int) -> None:
    kategori = get_kategori(db, kategori_id)
    try:
        repository.delete(db, kategori)
        db.commit()
        invalidate_kategori_cache()
    except IntegrityError as exc:
        db.rollback()
        raise BadRequestException("Kategori masih digunakan produk") from exc


def invalidate_kategori_cache() -> None:
    delete_pattern("kategori:*")
    delete_pattern("produk:public:*")
