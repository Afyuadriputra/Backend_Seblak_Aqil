from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import BigIntPrimaryKey, IdMixin, TimestampMixin, utc_now


class PesananTimeline(IdMixin, TimestampMixin, Base):
    __tablename__ = "pesanan_timeline"

    pesanan_id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("pesanan.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    tipe_event: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    judul: Mapped[str] = mapped_column(String(150), nullable=False)
    deskripsi: Mapped[str] = mapped_column(Text, nullable=False)
    waktu: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    actor_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="system",
        index=True,
    )
    admin_id: Mapped[int | None] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("admin.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )

    pesanan = relationship("Pesanan", back_populates="timeline")
    admin = relationship("Admin")

    __table_args__ = (
        Index("idx_pesanan_timeline_pesanan_waktu", "pesanan_id", "waktu"),
        Index("idx_pesanan_timeline_status", "status"),
    )
