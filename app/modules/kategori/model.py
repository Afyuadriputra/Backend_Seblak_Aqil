from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import IdMixin, TimestampMixin


class Kategori(IdMixin, TimestampMixin, Base):
    __tablename__ = "kategori"

    nama_kategori: Mapped[str] = mapped_column(String(100), nullable=False)
    deskripsi: Mapped[str | None] = mapped_column(Text, nullable=True)

    produk = relationship(
        "Produk",
        back_populates="kategori",
        cascade="save-update, merge",
    )
