from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.inventory.domain.enums import MovementType


class MovementResponse(BaseModel):
    """Schema for movement responses."""

    @field_validator("quantity", mode="before")
    @classmethod
    def get_quantity_value(cls, v: Any) -> Decimal:
        return Decimal(v.value) if hasattr(v, "value") else Decimal(v)

    id: UUID = Field(..., description="Unique identifier for the movement")
    item_id: UUID = Field(..., description="ID of the related item")
    warehouse_id: UUID = Field(..., description="ID of the related warehouse")
    quantity: Decimal = Field(..., gt=0, description="Movement quantity")
    movement_type: MovementType = Field(..., description="Type of movement")
    occurred_at: datetime = Field(..., description="Date and time of the movement")

    model_config = ConfigDict(from_attributes=True)


class RegisterMovementRequest(BaseModel):
    """Schema for registering a new movement."""

    item_id: UUID = Field(..., description="ID of the related item")
    warehouse_id: UUID = Field(..., description="ID of the related warehouse")
    quantity: Decimal = Field(..., gt=0, description="Movement quantity")
    movement_type: MovementType = Field(..., description="Type of movement")
    occurred_at: datetime = Field(..., description="Date and time of the movement")


class SearchMovementsResponse(BaseModel):
    """Schema for paginated movements search results."""

    data: list[MovementResponse]
    meta: dict[str, int]
