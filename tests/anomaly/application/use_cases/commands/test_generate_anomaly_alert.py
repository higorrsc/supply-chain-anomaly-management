import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from src.anomaly.application.use_cases.commands.generate_anomaly_alert import (
    GenerateAnomalyAlertRequestDTO,
    GenerateAnomalyAlertUseCase,
)
from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.domain.repositories.i_anomaly_alert import IAnomalyAlertRepository


class TestGenerateAnomalyAlertUseCase:
    """Test suite for GenerateAnomalyAlertUseCase."""

    @pytest.mark.asyncio
    async def test_generate_alert_successfully(self) -> None:
        """Test generating an anomaly alert successfully."""
        repository = AsyncMock(spec=IAnomalyAlertRepository)

        async def mock_save(alert: AnomalyAlert) -> AnomalyAlert:
            return alert

        repository.save.side_effect = mock_save

        use_case = GenerateAnomalyAlertUseCase(repository=repository)

        anomaly_id = uuid.uuid4()
        generated_at = datetime.now(UTC)

        request = GenerateAnomalyAlertRequestDTO(
            anomaly_id=anomaly_id,
            message="High deviation detected",
            generated_at=generated_at,
        )

        saved_alert = await use_case.execute(request)

        repository.save.assert_awaited_once()

        assert saved_alert.anomaly_id == anomaly_id
        assert saved_alert.message == "High deviation detected"
        assert saved_alert.is_read is False
