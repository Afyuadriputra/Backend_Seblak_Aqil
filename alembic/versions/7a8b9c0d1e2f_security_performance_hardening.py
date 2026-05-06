"""security performance hardening

Revision ID: 7a8b9c0d1e2f
Revises: 2c7e8d9f0a12
Create Date: 2026-05-06 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7a8b9c0d1e2f"
down_revision: str | Sequence[str] | None = "2c7e8d9f0a12"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    op.add_column(
        "admin",
        sa.Column("role", sa.String(length=30), nullable=False, server_default="admin"),
    )
    op.add_column(
        "admin",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    admin_count = bind.execute(sa.text("SELECT COUNT(*) FROM admin")).scalar() or 0
    if admin_count == 1:
        bind.execute(sa.text("UPDATE admin SET role = 'superadmin'"))

    op.create_index("idx_admin_role", "admin", ["role"], unique=False)
    op.create_index("idx_admin_is_active", "admin", ["is_active"], unique=False)

    op.create_index(
        "idx_produk_kategori_status", "produk", ["kategori_id", "status_tersedia"], unique=False
    )
    op.create_index(
        "idx_pesanan_status_pesanan_tanggal",
        "pesanan",
        ["status_pesanan", "tanggal_pesanan"],
        unique=False,
    )
    op.create_index(
        "idx_pesanan_status_pembayaran_tanggal",
        "pesanan",
        ["status_pembayaran", "tanggal_pesanan"],
        unique=False,
    )
    op.create_index(
        "idx_bukti_pembayaran_diupload", "bukti_pembayaran", ["diunggah_pada"], unique=False
    )
    op.create_index(
        "idx_bukti_pembayaran_dibuat", "bukti_pembayaran", ["dibuat_pada"], unique=False
    )
    op.create_index("idx_riwayat_stok_dibuat", "riwayat_stok", ["dibuat_pada"], unique=False)
    op.create_index("idx_audit_log_dibuat", "audit_log", ["dibuat_pada"], unique=False)

    if bind.dialect.name != "sqlite":
        op.create_check_constraint("ck_produk_stok_non_negative", "produk", "stok >= 0")


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()

    if bind.dialect.name != "sqlite":
        op.drop_constraint("ck_produk_stok_non_negative", "produk", type_="check")

    op.drop_index("idx_audit_log_dibuat", table_name="audit_log")
    op.drop_index("idx_riwayat_stok_dibuat", table_name="riwayat_stok")
    op.drop_index("idx_bukti_pembayaran_dibuat", table_name="bukti_pembayaran")
    op.drop_index("idx_bukti_pembayaran_diupload", table_name="bukti_pembayaran")
    op.drop_index("idx_pesanan_status_pembayaran_tanggal", table_name="pesanan")
    op.drop_index("idx_pesanan_status_pesanan_tanggal", table_name="pesanan")
    op.drop_index("idx_produk_kategori_status", table_name="produk")
    op.drop_index("idx_admin_is_active", table_name="admin")
    op.drop_index("idx_admin_role", table_name="admin")
    op.drop_column("admin", "is_active")
    op.drop_column("admin", "role")
