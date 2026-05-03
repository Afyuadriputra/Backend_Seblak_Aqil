from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import BigIntPrimaryKey, IdMixin, TimestampMixin


class Produk(IdMixin, TimestampMixin, Base):
    __tablename__ = "produk"

    kategori_id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("kategori.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    nama_produk: Mapped[str] = mapped_column(String(150), nullable=False)
    deskripsi: Mapped[str | None] = mapped_column(Text, nullable=True)
    harga: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    stok: Mapped[int] = mapped_column(nullable=False, default=0)
    gambar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status_tersedia: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
    )

    kategori = relationship(
        "Kategori",
        back_populates="produk",
    )

    detail_pesanan = relationship(
        "DetailPesanan",
        back_populates="produk",
        cascade="save-update, merge",
    )

    riwayat_stok = relationship(
        "RiwayatStok",
        back_populates="produk",
        cascade="save-update, merge",
    )

    @property
    def nama_kategori(self) -> str | None:
        return self.kategori.nama_kategori if self.kategori else None

    __table_args__ = (
        Index("idx_produk_kategori_id", "kategori_id"),
        Index("idx_produk_status_tersedia", "status_tersedia"),
    )
