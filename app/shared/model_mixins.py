from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.datetime_utils import utc_now

BigIntPrimaryKey = BigInteger().with_variant(Integer, "sqlite")


class IdMixin:
    id: Mapped[int] = mapped_column(
        BigIntPrimaryKey,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )


class TimestampMixin:
    dibuat_pada: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=True,
    )

    diperbarui_pada: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=True,
    )
