from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import BigIntPrimaryKey, IdMixin, TimestampMixin


class RiwayatStok(IdMixin, TimestampMixin, Base):
    __tablename__ = "riwayat_stok"

    produk_id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("produk.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    admin_id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("admin.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    jenis_perubahan: Mapped[str] = mapped_column(String(30), nullable=False)
    stok_sebelum: Mapped[int] = mapped_column(nullable=False)
    jumlah_perubahan: Mapped[int] = mapped_column(nullable=False)
    stok_sesudah: Mapped[int] = mapped_column(nullable=False)
    keterangan: Mapped[str | None] = mapped_column(Text, nullable=True)

    produk = relationship(
        "Produk",
        back_populates="riwayat_stok",
    )

    admin = relationship(
        "Admin",
        back_populates="riwayat_stok",
    )

    __table_args__ = (
        Index("idx_riwayat_stok_produk_id", "produk_id"),
        Index("idx_riwayat_stok_admin_id", "admin_id"),
    )
