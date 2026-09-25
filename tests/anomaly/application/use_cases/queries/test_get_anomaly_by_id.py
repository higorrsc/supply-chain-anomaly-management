import uuid
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.anomaly.application.exceptions import AnomalyNotFoundError
from src.anomaly.application.use_cases.queries.get_anomaly_by_id import (
    GetAnomalyByIdUseCase,
)
from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository
from src.anomaly.domain.value_objects.score import Score
from src.core.application.use_cases.queries.generic_get_by_id import GetByIdRequestDTO


class TestGetAnomalyByIdUseCase:
    """Test suite for GetAnomalyByIdUseCase."""

    @pytest.mark.asyncio
    async def test_get_anomaly_by_id_success(self) -> None:
        """Test getting an anomaly by ID successfully."""
        repository = AsyncMock(spec=IAnomalyRepository)

        anomaly_id = uuid.uuid4()
        existing_anomaly = Anomaly(
            id=anomaly_id,
            movement_id=uuid.uuid4(),
            item_id=uuid.uuid4(),
            score=Score(value=Decimal("80.5")),
            severity=AnomalySeverity.HIGH,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )
        repository.get_by_id.return_value = existing_anomaly

        use_case = GetAnomalyByIdUseCase(repository=repository)
        request = GetByIdRequestDTO(id=anomaly_id)

        result = await use_case.execute(request)

        repository.get_by_id.assert_awaited_once_with(entity_id=anomaly_id)
        assert result.id == anomaly_id
        assert result.severity == AnomalySeverity.HIGH

    @pytest.mark.asyncio
    async def test_get_anomaly_by_id_not_found(self) -> None:
        """Test getting an anomaly by ID when not found."""
        repository = AsyncMock(spec=IAnomalyRepository)
        repository.get_by_id.return_value = None

        use_case = GetAnomalyByIdUseCase(repository=repository)
        request = GetByIdRequestDTO(id=uuid.uuid4())

        with pytest.raises(AnomalyNotFoundError):
            await use_case.execute(request)
