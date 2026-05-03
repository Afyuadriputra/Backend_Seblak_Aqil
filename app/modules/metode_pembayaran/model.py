from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import IdMixin, TimestampMixin


class MetodePembayaran(IdMixin, TimestampMixin, Base):
    __tablename__ = "metode_pembayaran"

    nama_metode: Mapped[str] = mapped_column(String(100), nullable=False)
    tipe_metode: Mapped[str] = mapped_column(String(30), nullable=False)

    nama_bank: Mapped[str | None] = mapped_column(String(100), nullable=True)
    nomor_rekening: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nama_pemilik_rekening: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gambar_qr: Mapped[str | None] = mapped_column(String(255), nullable=True)

    status_aktif: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
    )

    pesanan = relationship(
        "Pesanan",
        back_populates="metode_pembayaran",
        cascade="save-update, merge",
    )
