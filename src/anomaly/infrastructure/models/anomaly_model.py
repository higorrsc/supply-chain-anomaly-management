import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.infrastructure.database import Base


class AnomalyModel(Base):
    """SQLAlchemy model for Anomaly."""

    __tablename__ = "anomalies"

    movement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("movements.id"),
        index=True,
        nullable=False,
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("items.id"),
        index=True,
        nullable=False,
    )
    score: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
