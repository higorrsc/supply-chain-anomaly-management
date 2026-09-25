from pydantic import BaseModel, Field


class AnomalyThresholds(BaseModel):
    low: float = Field(
        ...,
        description=(
            "Threshold for LOW severity anomaly (e.g. standard deviation multiplier)"
        ),
    )
    high: float = Field(..., description="Threshold for HIGH severity anomaly")
    critical: float = Field(..., description="Threshold for CRITICAL severity anomaly")


class AnomalyRules(BaseModel):
    enabled: bool = Field(
        default=True, description="Whether anomaly detection is enabled"
    )
    deviation_thresholds: AnomalyThresholds
