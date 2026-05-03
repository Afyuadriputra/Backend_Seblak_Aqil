from sqlalchemy.orm import Session

from app.modules.pelanggan import repository
from app.modules.pelanggan.model import Pelanggan
from app.shared.exceptions import NotFoundException


def list_pelanggan(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    search: str | None = None,
) -> tuple[list[Pelanggan], int]:
    return repository.list_all(db, offset, limit, search), repository.count_all(db, search)


def get_pelanggan(db: Session, pelanggan_id: int) -> Pelanggan:
    pelanggan = repository.get_by_id(db, pelanggan_id)
    if pelanggan is None:
        raise NotFoundException("Pelanggan tidak ditemukan")
    return pelanggan
