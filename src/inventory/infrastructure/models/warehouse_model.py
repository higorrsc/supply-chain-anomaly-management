from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.infrastructure.database import Base


class WarehouseModel(Base):
    """SQLAlchemy model for Warehouse."""

    __tablename__ = "warehouses"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    location_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
