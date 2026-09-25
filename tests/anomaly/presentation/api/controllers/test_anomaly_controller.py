from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.anomaly.application.exceptions import AnomalyNotFoundError
from src.anomaly.application.use_cases.commands.register_anomaly import (
    RegisterAnomalyUseCase,
)
from src.anomaly.application.use_cases.commands.resolve_anomaly import (
    ResolveAnomalyUseCase,
)
from src.anomaly.application.use_cases.queries.get_alerts_by_anomaly_id import (
    GetAlertsByAnomalyIdUseCase,
)
from src.anomaly.application.use_cases.queries.get_anomaly_by_id import (
    GetAnomalyByIdUseCase,
)
from src.anomaly.application.use_cases.queries.search_anomaly import (
    SearchAnomalyUseCase,
)
from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.value_objects.score import Score
from src.anomaly.presentation.api.controllers.anomaly_controller import router
from src.anomaly.presentation.api.dependencies import (
    get_alerts_by_anomaly_id_use_case,
    get_anomaly_by_id_use_case,
    get_register_anomaly_use_case,
    get_resolve_anomaly_use_case,
    get_search_anomaly_use_case,
)
from src.core.application.use_cases.queries.generic_search import SearchResponseDTO

# Setup FastAPI app for testing
app = FastAPI()
app.include_router(router)

# Mock Use Cases
mock_register_uc = AsyncMock(spec=RegisterAnomalyUseCase)
mock_get_by_id_uc = AsyncMock(spec=GetAnomalyByIdUseCase)
mock_resolve_uc = AsyncMock(spec=ResolveAnomalyUseCase)
mock_search_uc = AsyncMock(spec=SearchAnomalyUseCase)
mock_alerts_uc = AsyncMock(spec=GetAlertsByAnomalyIdUseCase)

app.dependency_overrides[get_register_anomaly_use_case] = lambda: mock_register_uc
app.dependency_overrides[get_anomaly_by_id_use_case] = lambda: mock_get_by_id_uc
app.dependency_overrides[get_resolve_anomaly_use_case] = lambda: mock_resolve_uc
app.dependency_overrides[get_search_anomaly_use_case] = lambda: mock_search_uc
app.dependency_overrides[get_alerts_by_anomaly_id_use_case] = lambda: mock_alerts_uc


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


class TestAnomalyController:
    @pytest.mark.asyncio
    async def test_register_anomaly(self, client: AsyncClient) -> None:
        movement_id = uuid4()
        item_id = uuid4()
        detected_at = datetime.now(UTC)

        anomaly = Anomaly(
            movement_id=movement_id,
            item_id=item_id,
            score=Score(value=Decimal("85.5")),
            severity=AnomalySeverity.HIGH,
            status=AnomalyStatus.OPEN,
            detected_at=detected_at,
        )
        mock_register_uc.execute.return_value = anomaly

        payload = {
            "movement_id": str(movement_id),
            "item_id": str(item_id),
            "score": "85.5",
            "severity": "high",
            "detected_at": detected_at.isoformat(),
        }

        response = await client.post("/anomalies", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == str(anomaly.id)
        assert data["severity"] == AnomalySeverity.HIGH.value
        assert data["status"] == AnomalyStatus.OPEN.value

    @pytest.mark.asyncio
    async def test_get_anomaly_by_id_success(self, client: AsyncClient) -> None:
        anomaly = Anomaly(
            movement_id=uuid4(),
            item_id=uuid4(),
            score=Score(value=Decimal("99.0")),
            severity=AnomalySeverity.CRITICAL,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )
        mock_get_by_id_uc.execute.return_value = anomaly

        response = await client.get(f"/anomalies/{anomaly.id}")
        assert response.status_code == 200
        assert response.json()["id"] == str(anomaly.id)

    @pytest.mark.asyncio
    async def test_get_anomaly_by_id_not_found(self, client: AsyncClient) -> None:
        mock_get_by_id_uc.execute.side_effect = AnomalyNotFoundError(uuid4())

        response = await client.get(f"/anomalies/{uuid4()}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_resolve_anomaly(self, client: AsyncClient) -> None:
        anomaly = Anomaly(
            movement_id=uuid4(),
            item_id=uuid4(),
            score=Score(value=Decimal("99.0")),
            severity=AnomalySeverity.CRITICAL,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )
        anomaly.resolve()
        mock_resolve_uc.execute.return_value = anomaly

        response = await client.put(f"/anomalies/{anomaly.id}/resolve")
        assert response.status_code == 200
        assert response.json()["status"] == "resolved"

    @pytest.mark.asyncio
    async def test_get_alerts_by_anomaly_id(self, client: AsyncClient) -> None:
        anomaly_id = uuid4()
        alert = AnomalyAlert(
            anomaly_id=anomaly_id,
            message="Test alert",
            is_read=False,
            generated_at=datetime.now(UTC),
        )
        mock_alerts_uc.execute.return_value = [alert]

        response = await client.get(f"/anomalies/{anomaly_id}/alerts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["message"] == "Test alert"

    @pytest.mark.asyncio
    async def test_search_anomalies(self, client: AsyncClient) -> None:
        anomaly = Anomaly(
            movement_id=uuid4(),
            item_id=uuid4(),
            score=Score(value=Decimal("99.0")),
            severity=AnomalySeverity.CRITICAL,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )
        page_response = SearchResponseDTO(
            data=[anomaly],
            meta={
                "total_items": 1,
                "page": 1,
                "page_size": 10,
                "total_pages": 1,
            },
        )
        mock_search_uc.execute.return_value = page_response

        response = await client.get("/anomalies?severity=CRITICAL")
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["total_items"] == 1
        assert len(data["data"]) == 1
        assert data["data"][0]["severity"] == "critical"
