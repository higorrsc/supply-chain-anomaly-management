import uuid
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.anomaly.application.use_cases.commands.register_anomaly import (
    RegisterAnomalyRequestDTO,
    RegisterAnomalyUseCase,
)
from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository


class TestRegisterAnomalyUseCase:
    """Test suite for RegisterAnomalyUseCase."""

    @pytest.mark.asyncio
    async def test_execute_use_case_successfully(self) -> None:
        """Test registering an anomaly successfully."""
        repository = AsyncMock(spec=IAnomalyRepository)

        # Setup mock to return the passed anomaly on save
        async def mock_save(anomaly: Anomaly) -> Anomaly:
            return anomaly

        repository.save.side_effect = mock_save

        use_case = RegisterAnomalyUseCase(repository=repository)

        movement_id = uuid.uuid4()
        item_id = uuid.uuid4()
        detected_at = datetime.now(UTC)

        request = RegisterAnomalyRequestDTO(
            movement_id=movement_id,
            item_id=item_id,
            score=Decimal("95.0"),
            severity=AnomalySeverity.CRITICAL,
            detected_at=detected_at,
        )

        saved_anomaly = await use_case.execute(request)

        repository.save.assert_awaited_once()

        assert saved_anomaly.movement_id == movement_id
        assert saved_anomaly.score.value == Decimal("95.0")
        assert saved_anomaly.severity == AnomalySeverity.CRITICAL
        assert saved_anomaly.status == AnomalyStatus.OPEN
