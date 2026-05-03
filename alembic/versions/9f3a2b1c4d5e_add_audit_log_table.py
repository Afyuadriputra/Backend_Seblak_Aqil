"""add audit log table

Revision ID: 9f3a2b1c4d5e
Revises: 561f0b46d411
Create Date: 2026-05-04 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f3a2b1c4d5e"
down_revision: str | Sequence[str] | None = "561f0b46d411"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "audit_log",
        sa.Column("admin_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=True),
        sa.Column("aksi", sa.String(length=100), nullable=False),
        sa.Column("entity", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("deskripsi", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("dibuat_pada", sa.DateTime(timezone=True), nullable=True),
        sa.Column("diperbarui_pada", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["admin_id"],
            ["admin.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_audit_aksi", "audit_log", ["aksi"], unique=False)
    op.create_index("idx_audit_entity", "audit_log", ["entity", "entity_id"], unique=False)
    op.create_index(op.f("ix_audit_log_admin_id"), "audit_log", ["admin_id"], unique=False)
    op.create_index(op.f("ix_audit_log_aksi"), "audit_log", ["aksi"], unique=False)
    op.create_index(op.f("ix_audit_log_entity"), "audit_log", ["entity"], unique=False)
    op.create_index(op.f("ix_audit_log_entity_id"), "audit_log", ["entity_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_audit_log_entity_id"), table_name="audit_log")
    op.drop_index(op.f("ix_audit_log_entity"), table_name="audit_log")
    op.drop_index(op.f("ix_audit_log_aksi"), table_name="audit_log")
    op.drop_index(op.f("ix_audit_log_admin_id"), table_name="audit_log")
    op.drop_index("idx_audit_entity", table_name="audit_log")
    op.drop_index("idx_audit_aksi", table_name="audit_log")
    op.drop_table("audit_log")
