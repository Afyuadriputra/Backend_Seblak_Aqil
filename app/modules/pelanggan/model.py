from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import IdMixin, TimestampMixin


class Pelanggan(IdMixin, TimestampMixin, Base):
    __tablename__ = "pelanggan"

    nama_pelanggan: Mapped[str] = mapped_column(String(100), nullable=False)
    no_telepon: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    alamat: Mapped[str] = mapped_column(Text, nullable=False)

    pesanan = relationship(
        "Pesanan",
        back_populates="pelanggan",
        cascade="save-update, merge",
    )
