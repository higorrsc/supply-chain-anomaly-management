import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from src.anomaly.application.use_cases.queries.get_alerts_by_anomaly_id import (
    GetAlertsByAnomalyIdUseCase,
)
from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.domain.repositories.i_anomaly_alert import IAnomalyAlertRepository


class TestGetAlertsByAnomalyIdUseCase:
    """Test suite for GetAlertsByAnomalyIdUseCase."""

    @pytest.mark.asyncio
    async def test_get_alerts_success(self) -> None:
        """Test getting alerts by anomaly id successfully."""
        repository = AsyncMock(spec=IAnomalyAlertRepository)

        anomaly_id = uuid.uuid4()
        alert = AnomalyAlert(
            id=uuid.uuid4(),
            anomaly_id=anomaly_id,
            message="Alert message",
            is_read=False,
            generated_at=datetime.now(UTC),
        )

        repository.get_by_anomaly_id.return_value = [alert]

        use_case = GetAlertsByAnomalyIdUseCase(repository=repository)
        result = await use_case.execute(anomaly_id)

        repository.get_by_anomaly_id.assert_awaited_once_with(anomaly_id)
        assert len(result) == 1
        assert result[0] == alert

    @pytest.mark.asyncio
    async def test_get_alerts_empty(self) -> None:
        """Test getting alerts by anomaly id when none exist."""
        repository = AsyncMock(spec=IAnomalyAlertRepository)
        repository.get_by_anomaly_id.return_value = []

        use_case = GetAlertsByAnomalyIdUseCase(repository=repository)
        result = await use_case.execute(uuid.uuid4())

        assert len(result) == 0
