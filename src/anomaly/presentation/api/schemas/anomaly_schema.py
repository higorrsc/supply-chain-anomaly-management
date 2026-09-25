from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus


class SearchAnomaliesResponse(BaseModel):
    data: list[AnomalyResponse]
    meta: dict[str, int]


class AnomalyResponse(BaseModel):
    """Schema for anomaly responses."""

    @field_validator("score", mode="before")
    @classmethod
    def get_score_value(cls, v: Any) -> Decimal:
        return Decimal(v.value) if hasattr(v, "value") else Decimal(v)

    id: UUID = Field(..., description="Unique identifier for the anomaly")
    movement_id: UUID = Field(..., description="ID of the related stock movement")
    item_id: UUID = Field(..., description="ID of the related item")
    score: Decimal = Field(..., ge=0, le=100, description="Anomaly score")
    severity: AnomalySeverity = Field(..., description="Severity of the anomaly")
    status: AnomalyStatus = Field(..., description="Current status of the anomaly")
    detected_at: datetime = Field(..., description="Date and time of detection")

    model_config = ConfigDict(from_attributes=True)


class AnomalyAlertResponse(BaseModel):
    """Schema for anomaly alert responses."""

    id: UUID = Field(..., description="Unique identifier for the alert")
    anomaly_id: UUID = Field(..., description="ID of the related anomaly")
    message: str = Field(..., description="Alert message")
    is_read: bool = Field(..., description="Whether the alert has been read")
    generated_at: datetime = Field(..., description="Date and time of generation")

    model_config = ConfigDict(from_attributes=True)


class RegisterAnomalyRequest(BaseModel):
    """Schema for registering a new anomaly."""

    movement_id: UUID = Field(..., description="ID of the related stock movement")
    item_id: UUID = Field(..., description="ID of the related item")
    score: Decimal = Field(..., ge=0, le=100, description="Anomaly score")
    severity: AnomalySeverity = Field(..., description="Severity of the anomaly")
    detected_at: datetime = Field(..., description="Date and time of detection")
