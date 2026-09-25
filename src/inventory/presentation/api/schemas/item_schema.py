from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ItemResponse(BaseModel):
    """Schema for item responses."""

    @field_validator("sku", mode="before")
    @classmethod
    def get_sku_value(cls, v: Any) -> str:
        return str(v.value) if hasattr(v, "value") else str(v)

    id: UUID = Field(..., description="Unique identifier for the item")
    sku: str = Field(..., description="Stock Keeping Unit")
    description: str = Field(..., description="Item description")
    is_active: bool = Field(..., description="Whether the item is active")

    model_config = ConfigDict(from_attributes=True)


class RegisterItemRequest(BaseModel):
    """Schema for registering a new item."""

    sku: str = Field(..., description="Stock Keeping Unit")
    description: str = Field(..., description="Item description")
    is_active: bool = Field(True, description="Whether the item is active")


class UpdateItemRequest(BaseModel):
    """Schema for updating an existing item."""

    description: str = Field(..., description="Item description")


class SearchItemsResponse(BaseModel):
    """Schema for paginated items search results."""

    data: list[ItemResponse]
    meta: dict[str, int]
