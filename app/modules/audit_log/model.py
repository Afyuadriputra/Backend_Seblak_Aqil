from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import BigIntPrimaryKey, IdMixin, TimestampMixin


class AuditLog(IdMixin, TimestampMixin, Base):
    __tablename__ = "audit_log"

    admin_id: Mapped[int | None] = mapped_column(
        BigIntPrimaryKey,
        ForeignKey("admin.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )
    aksi: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    deskripsi: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    admin = relationship("Admin")

    __table_args__ = (
        Index("idx_audit_entity", "entity", "entity_id"),
        Index("idx_audit_aksi", "aksi"),
    )
