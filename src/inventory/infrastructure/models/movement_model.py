import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.infrastructure.database import Base


class MovementModel(Base):
    """SQLAlchemy model for Movement."""

    __tablename__ = "movements"

    item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("items.id"),
        index=True,
        nullable=False,
    )
    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        index=True,
        nullable=False,
    )
    quantity: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    movement_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
