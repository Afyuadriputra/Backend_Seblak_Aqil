from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.enums import AdminRole
from app.shared.model_mixins import IdMixin, TimestampMixin


class Admin(IdMixin, TimestampMixin, Base):
    __tablename__ = "admin"

    nama_admin: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    kata_sandi: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=AdminRole.ADMIN.value,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
    )

    riwayat_stok = relationship(
        "RiwayatStok",
        back_populates="admin",
        cascade="save-update, merge",
    )
