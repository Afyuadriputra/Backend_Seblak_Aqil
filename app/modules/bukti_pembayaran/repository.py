from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.bukti_pembayaran.model import BuktiPembayaran


def list_by_pesanan_id(db: Session, pesanan_id: int) -> list[BuktiPembayaran]:
    return list(
        db.scalars(
            select(BuktiPembayaran)
            .where(BuktiPembayaran.pesanan_id == pesanan_id)
            .order_by(BuktiPembayaran.diunggah_pada.desc(), BuktiPembayaran.id.desc())
        )
    )


def count_by_pesanan_id(db: Session, pesanan_id: int) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(BuktiPembayaran)
            .where(BuktiPembayaran.pesanan_id == pesanan_id)
        )
        or 0
    )


def get_by_id(db: Session, bukti_id: int) -> BuktiPembayaran | None:
    return db.get(BuktiPembayaran, bukti_id)


def create(db: Session, data: dict) -> BuktiPembayaran:
    bukti = BuktiPembayaran(**data)
    db.add(bukti)
    db.flush()
    return bukti


def delete(db: Session, bukti: BuktiPembayaran) -> None:
    db.delete(bukti)
    db.flush()
