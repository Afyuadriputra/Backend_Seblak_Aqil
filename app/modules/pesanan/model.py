from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.enums import StatusPembayaran, StatusPesanan
from app.shared.model_mixins import BigIntPrimaryKey, IdMixin, TimestampMixin, utc_now


class Pesanan(IdMixin, TimestampMixin, Base):
    __tablename__ = "pesanan"

    pelanggan_id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("pelanggan.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    metode_pembayaran_id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("metode_pembayaran.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    kode_pesanan: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    tanggal_pesanan: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    total_harga: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    nama_pelanggan: Mapped[str] = mapped_column(String(100), nullable=False)
    no_telepon_pelanggan: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    alamat_pelanggan: Mapped[str] = mapped_column(Text, nullable=False)

    catatan: Mapped[str | None] = mapped_column(Text, nullable=True)

    status_pembayaran: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=StatusPembayaran.BELUM_DIBAYAR.value,
        index=True,
    )

    status_pesanan: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=StatusPesanan.MENUNGGU_KONFIRMASI.value,
        index=True,
    )

    pelanggan = relationship(
        "Pelanggan",
        back_populates="pesanan",
    )

    metode_pembayaran = relationship(
        "MetodePembayaran",
        back_populates="pesanan",
    )

    detail_pesanan = relationship(
        "DetailPesanan",
        back_populates="pesanan",
        cascade="all, delete-orphan",
    )

    bukti_pembayaran = relationship(
        "BuktiPembayaran",
        back_populates="pesanan",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_lacak_pesanan", "kode_pesanan", "no_telepon_pelanggan"),
        Index("idx_pesanan_status_pembayaran", "status_pembayaran"),
        Index("idx_pesanan_status_pesanan", "status_pesanan"),
        Index("idx_pesanan_tanggal", "tanggal_pesanan"),
    )


class DetailPesanan(IdMixin, TimestampMixin, Base):
    __tablename__ = "detail_pesanan"

    pesanan_id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("pesanan.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    produk_id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("produk.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    nama_produk: Mapped[str] = mapped_column(String(150), nullable=False)
    harga_produk: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    jumlah: Mapped[int] = mapped_column(nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    pesanan = relationship(
        "Pesanan",
        back_populates="detail_pesanan",
    )

    produk = relationship(
        "Produk",
        back_populates="detail_pesanan",
    )

    __table_args__ = (
        Index("idx_detail_pesanan_pesanan_id", "pesanan_id"),
        Index("idx_detail_pesanan_produk_id", "produk_id"),
    )
