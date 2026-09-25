import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.infrastructure.database import Base


class AnomalyAlertModel(Base):
    """SQLAlchemy model for AnomalyAlert."""

    __tablename__ = "anomaly_alerts"

    anomaly_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("anomalies.id"),
        index=True,
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
