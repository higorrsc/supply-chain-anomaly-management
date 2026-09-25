import uuid
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.anomaly.application.use_cases.queries.search_anomaly import (
    SearchAnomalyUseCase,
)
from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository
from src.anomaly.domain.value_objects.score import Score
from src.core.application.use_cases.queries.generic_search import SearchRequestDTO
from src.core.domain.repository import Page, PageRequest


class TestSearchAnomalyUseCase:
    """Test suite for SearchAnomalyUseCase."""

    @pytest.mark.asyncio
    async def test_search_anomaly_success(self) -> None:
        """Test searching anomalies successfully."""
        repository = AsyncMock(spec=IAnomalyRepository)

        anomaly = Anomaly(
            id=uuid.uuid4(),
            movement_id=uuid.uuid4(),
            item_id=uuid.uuid4(),
            score=Score(value=Decimal("80.5")),
            severity=AnomalySeverity.HIGH,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )

        expected_page = Page(items=[anomaly], total_items=1, page=1, page_size=10)
        repository.search.return_value = expected_page

        use_case = SearchAnomalyUseCase(repository=repository)
        criteria = SearchRequestDTO(filters={}, page=1, page_size=10)

        result = await use_case.execute(criteria)

        from src.core.domain.repository import SearchCriteria

        repository.search.assert_awaited_once_with(
            criteria=SearchCriteria(
                filters={}, pagination=PageRequest(page=1, page_size=10)
            )
        )
        assert result.meta["total_items"] == 1
        assert len(result.data) == 1
        assert result.data[0] == anomaly
