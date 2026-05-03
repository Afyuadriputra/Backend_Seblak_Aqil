from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import BigIntPrimaryKey, IdMixin, TimestampMixin, utc_now


class BuktiPembayaran(IdMixin, TimestampMixin, Base):
    __tablename__ = "bukti_pembayaran"

    pesanan_id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("pesanan.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    nama_file: Mapped[str] = mapped_column(String(255), nullable=False)
    path_file: Mapped[str] = mapped_column(String(255), nullable=False)

    diunggah_pada: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    pesanan = relationship(
        "Pesanan",
        back_populates="bukti_pembayaran",
    )

    __table_args__ = (Index("idx_bukti_pembayaran_pesanan_id", "pesanan_id"),)
