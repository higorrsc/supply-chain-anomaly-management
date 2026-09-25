import logging
from datetime import UTC, datetime

from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository
from src.anomaly.domain.rules import AnomalyRules
from src.anomaly.domain.services.analysis import MovementAnomalyAnalysisService
from src.inventory.domain.events import MovementCreatedEvent

logger = logging.getLogger(__name__)


class DetectAnomalyForMovementHandler:
    def __init__(self, repository: IAnomalyRepository, rules: AnomalyRules) -> None:
        self.repository = repository
        self.rules = rules
        self.analysis_service = MovementAnomalyAnalysisService(rules)

    async def handle(self, event: MovementCreatedEvent) -> None:
        try:
            severity, score = self.analysis_service.analyze(event)
            if severity and score:
                anomaly = Anomaly(
                    movement_id=event.movement_id,
                    item_id=event.item_id,
                    score=score,
                    detected_at=datetime.now(UTC),
                    severity=severity,
                )
                await self.repository.save(anomaly)
                logger.info(
                    f"Anomaly detected for item {event.item_id} "
                    f"with severity {severity}"
                )
        except Exception as e:
            logger.error(
                f"Error handling MovementCreatedEvent for anomaly detection: {e}"
            )
            raise
