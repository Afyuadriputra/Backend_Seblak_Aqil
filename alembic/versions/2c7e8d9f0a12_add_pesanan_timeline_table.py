"""add pesanan timeline table

Revision ID: 2c7e8d9f0a12
Revises: 9f3a2b1c4d5e
Create Date: 2026-05-05 00:00:00.000000

"""

from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2c7e8d9f0a12"
down_revision: str | Sequence[str] | None = "9f3a2b1c4d5e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


ORDER_COPY = {
    "menunggu_konfirmasi": (
        "Order Placed",
        "Order berhasil dibuat.",
    ),
    "diproses": (
        "Order is being Prepared",
        "Dapur sedang menyiapkan pesanan Anda. Pesanan segera diproses.",
    ),
    "selesai": (
        "Siap Diambil / Diantar",
        "Pesanan sudah selesai dan siap diambil atau diantar.",
    ),
    "dibatalkan": (
        "Order Cancelled",
        "Pesanan dibatalkan.",
    ),
}

PAYMENT_COPY = {
    "belum_dibayar": (
        "Menunggu Pembayaran",
        "Pesanan dibuat. Silakan unggah bukti pembayaran agar pesanan bisa diverifikasi.",
    ),
    "menunggu_verifikasi": (
        "Bukti Pembayaran Diupload",
        "Bukti pembayaran sudah diterima dan menunggu verifikasi admin.",
    ),
    "diterima": (
        "Payment Verified",
        "Pembayaran sudah diterima dan diverifikasi.",
    ),
    "ditolak": (
        "Payment Rejected",
        "Pembayaran ditolak. Silakan unggah bukti pembayaran yang benar.",
    ),
}


def upgrade() -> None:
    """Upgrade schema."""
    big_int = sa.BigInteger().with_variant(sa.Integer(), "sqlite")
    op.create_table(
        "pesanan_timeline",
        sa.Column("pesanan_id", big_int, nullable=False),
        sa.Column("tipe_event", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("judul", sa.String(length=150), nullable=False),
        sa.Column("deskripsi", sa.Text(), nullable=False),
        sa.Column("waktu", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor_type", sa.String(length=30), nullable=False),
        sa.Column("admin_id", big_int, nullable=True),
        sa.Column("id", big_int, autoincrement=True, nullable=False),
        sa.Column("dibuat_pada", sa.DateTime(timezone=True), nullable=True),
        sa.Column("diperbarui_pada", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["admin_id"],
            ["admin.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["pesanan_id"],
            ["pesanan.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_pesanan_timeline_pesanan_waktu",
        "pesanan_timeline",
        ["pesanan_id", "waktu"],
        unique=False,
    )
    op.create_index("idx_pesanan_timeline_status", "pesanan_timeline", ["status"], unique=False)
    op.create_index(
        op.f("ix_pesanan_timeline_actor_type"),
        "pesanan_timeline",
        ["actor_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pesanan_timeline_admin_id"),
        "pesanan_timeline",
        ["admin_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pesanan_timeline_pesanan_id"),
        "pesanan_timeline",
        ["pesanan_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pesanan_timeline_status"),
        "pesanan_timeline",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pesanan_timeline_tipe_event"),
        "pesanan_timeline",
        ["tipe_event"],
        unique=False,
    )

    backfill_existing_orders()


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_pesanan_timeline_tipe_event"), table_name="pesanan_timeline")
    op.drop_index(op.f("ix_pesanan_timeline_status"), table_name="pesanan_timeline")
    op.drop_index(op.f("ix_pesanan_timeline_pesanan_id"), table_name="pesanan_timeline")
    op.drop_index(op.f("ix_pesanan_timeline_admin_id"), table_name="pesanan_timeline")
    op.drop_index(op.f("ix_pesanan_timeline_actor_type"), table_name="pesanan_timeline")
    op.drop_index("idx_pesanan_timeline_status", table_name="pesanan_timeline")
    op.drop_index("idx_pesanan_timeline_pesanan_waktu", table_name="pesanan_timeline")
    op.drop_table("pesanan_timeline")


def backfill_existing_orders() -> None:
    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            """
            SELECT
                id,
                tanggal_pesanan,
                dibuat_pada,
                diperbarui_pada,
                status_pembayaran,
                status_pesanan
            FROM pesanan
            """
        )
    ).mappings()

    timeline_table = sa.table(
        "pesanan_timeline",
        sa.column("pesanan_id", sa.Integer),
        sa.column("tipe_event", sa.String),
        sa.column("status", sa.String),
        sa.column("judul", sa.String),
        sa.column("deskripsi", sa.Text),
        sa.column("waktu", sa.DateTime),
        sa.column("actor_type", sa.String),
        sa.column("admin_id", sa.Integer),
        sa.column("dibuat_pada", sa.DateTime),
        sa.column("diperbarui_pada", sa.DateTime),
    )

    inserts = []
    for row in rows:
        created_at = coerce_datetime(row["tanggal_pesanan"] or row["dibuat_pada"])
        updated_at = coerce_datetime(row["diperbarui_pada"]) or created_at
        inserts.append(
            make_row(
                row["id"],
                "pesanan",
                "menunggu_konfirmasi",
                ORDER_COPY["menunggu_konfirmasi"],
                created_at,
            )
        )
        if row["status_pesanan"] != "menunggu_konfirmasi":
            inserts.append(
                make_row(
                    row["id"],
                    "pesanan",
                    row["status_pesanan"],
                    ORDER_COPY.get(
                        row["status_pesanan"],
                        ("Status Pesanan Diperbarui", "Status pesanan diperbarui."),
                    ),
                    updated_at,
                )
            )
        inserts.append(
            make_row(
                row["id"],
                "pembayaran",
                row["status_pembayaran"],
                PAYMENT_COPY.get(
                    row["status_pembayaran"],
                    ("Status Pembayaran Diperbarui", "Status pembayaran diperbarui."),
                ),
                updated_at if row["status_pembayaran"] != "belum_dibayar" else created_at,
            )
        )

    if inserts:
        op.bulk_insert(timeline_table, inserts)


def make_row(
    pesanan_id: int,
    tipe_event: str,
    status: str,
    copy: tuple[str, str],
    waktu,
) -> dict:
    return {
        "pesanan_id": pesanan_id,
        "tipe_event": tipe_event,
        "status": status,
        "judul": copy[0],
        "deskripsi": copy[1],
        "waktu": waktu,
        "actor_type": "system",
        "admin_id": None,
        "dibuat_pada": waktu,
        "diperbarui_pada": waktu,
    }


def coerce_datetime(value) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return datetime.now(UTC)
