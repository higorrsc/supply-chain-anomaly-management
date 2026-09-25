import uuid
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.anomaly.application.exceptions import AnomalyNotFoundError
from src.anomaly.application.use_cases.commands.resolve_anomaly import (
    ResolveAnomalyRequestDTO,
    ResolveAnomalyUseCase,
)
from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.exceptions import InvalidAnomalyError
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository
from src.anomaly.domain.value_objects.score import Score


class TestResolveAnomalyUseCase:
    """Test suite for ResolveAnomalyUseCase."""

    @pytest.mark.asyncio
    async def test_resolve_anomaly_successfully(self) -> None:
        """Test resolving an anomaly successfully."""
        repository = AsyncMock(spec=IAnomalyRepository)
        use_case = ResolveAnomalyUseCase(repository=repository)

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

        async def mock_save(anomaly: Anomaly) -> Anomaly:
            return anomaly

        repository.save.side_effect = mock_save

        request = ResolveAnomalyRequestDTO(anomaly_id=anomaly_id)
        saved_anomaly = await use_case.execute(request)

        repository.get_by_id.assert_awaited_once_with(anomaly_id)
        repository.save.assert_awaited_once_with(existing_anomaly)

        assert saved_anomaly.status == AnomalyStatus.RESOLVED

    @pytest.mark.asyncio
    async def test_resolve_anomaly_not_found(self) -> None:
        """Test resolving a non-existent anomaly."""
        repository = AsyncMock(spec=IAnomalyRepository)
        repository.get_by_id.return_value = None

        use_case = ResolveAnomalyUseCase(repository=repository)
        request = ResolveAnomalyRequestDTO(anomaly_id=uuid.uuid4())

        with pytest.raises(AnomalyNotFoundError):
            await use_case.execute(request)

    @pytest.mark.asyncio
    async def test_resolve_anomaly_already_resolved(self) -> None:
        """Test resolving an anomaly that is already resolved."""
        repository = AsyncMock(spec=IAnomalyRepository)

        anomaly_id = uuid.uuid4()
        existing_anomaly = Anomaly(
            id=anomaly_id,
            movement_id=uuid.uuid4(),
            item_id=uuid.uuid4(),
            score=Score(value=Decimal("80.5")),
            severity=AnomalySeverity.HIGH,
            status=AnomalyStatus.RESOLVED,
            detected_at=datetime.now(UTC),
        )
        repository.get_by_id.return_value = existing_anomaly

        use_case = ResolveAnomalyUseCase(repository=repository)
        request = ResolveAnomalyRequestDTO(anomaly_id=anomaly_id)

        with pytest.raises(InvalidAnomalyError):
            await use_case.execute(request)
