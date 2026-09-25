"""create movement model

Revision ID: 3535ec4fe300
Revises: 31b6e44e53cc
Create Date: 2026-09-24 15:42:14.376187

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3535ec4fe300"
down_revision: str | Sequence[str] | None = "31b6e44e53cc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "movements",
        sa.Column(
            "item_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "warehouse_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "quantity",
            sa.Numeric(precision=10, scale=2),
            nullable=False,
        ),
        sa.Column(
            "movement_type",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["items.id"],
        ),
        sa.ForeignKeyConstraint(
            ["warehouse_id"],
            ["warehouses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_movements_item_id"),
        "movements",
        ["item_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_movements_warehouse_id"),
        "movements",
        ["warehouse_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_movements_warehouse_id"),
        table_name="movements",
    )
    op.drop_index(
        op.f("ix_movements_item_id"),
        table_name="movements",
    )
    op.drop_table("movements")
