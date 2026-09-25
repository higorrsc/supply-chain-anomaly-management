from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WarehouseResponse(BaseModel):
    """Schema for warehouse responses."""

    id: UUID = Field(..., description="Unique identifier for the warehouse")
    name: str = Field(..., description="Warehouse name")
    location_code: str = Field(..., description="Location code of the warehouse")
    is_active: bool = Field(..., description="Whether the warehouse is active")

    model_config = ConfigDict(from_attributes=True)


class RegisterWarehouseRequest(BaseModel):
    """Schema for registering a new warehouse."""

    name: str = Field(..., description="Warehouse name")
    location_code: str = Field(..., description="Location code of the warehouse")
    is_active: bool = Field(True, description="Whether the warehouse is active")


class UpdateWarehouseRequest(BaseModel):
    """Schema for updating an existing warehouse."""

    name: str = Field(..., description="Warehouse name")
    location_code: str = Field(..., description="Location code of the warehouse")


class SearchWarehousesResponse(BaseModel):
    """Schema for paginated warehouses search results."""

    data: list[WarehouseResponse]
    meta: dict[str, int]
