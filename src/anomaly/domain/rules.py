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


class DeviationRule(BaseModel):
    enabled: bool = True
    thresholds: AnomalyThresholds


class BusinessHoursRule(BaseModel):
    enabled: bool = True
    start_time: str = "08:00"
    end_time: str = "18:00"


class MaxQuantityRule(BaseModel):
    enabled: bool = True
    max_in: int = 100
    max_out: int = 50


class RulesConfig(BaseModel):
    deviation: DeviationRule
    business_hours: BusinessHoursRule
    max_quantity: MaxQuantityRule


class AnomalyRules(BaseModel):
    enabled: bool = Field(
        default=True, description="Whether anomaly detection is enabled"
    )
    rules: RulesConfig
