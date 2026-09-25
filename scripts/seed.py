import asyncio
import random
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from src.anomaly.domain.entities import Anomaly
from src.anomaly.domain.services import MovementAnomalyAnalysisService
from src.anomaly.infrastructure.config import load_anomaly_rules
from src.anomaly.infrastructure.repositories import AnomalyRepository
from src.core.infrastructure.database import AsyncSessionLocal, Base, engine
from src.inventory.domain.entities import Item, Movement, Warehouse
from src.inventory.domain.enums import MovementType
from src.inventory.domain.events import MovementCreatedEvent
from src.inventory.domain.value_objects import SKU, Quantity

# Import models so Base.metadata.create_all works properly
from src.inventory.infrastructure.repositories import (
    ItemRepository,
    MovementRepository,
    WarehouseRepository,
)


async def seed_data() -> None:
    print("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("Loading anomaly rules...")
    rules = load_anomaly_rules("anomaly_rules.yaml")
    analysis_service = MovementAnomalyAnalysisService(rules=rules)

    async with AsyncSessionLocal() as session:
        item_repo = ItemRepository(session)
        warehouse_repo = WarehouseRepository(session)
        movement_repo = MovementRepository(session)
        anomaly_repo = AnomalyRepository(session)

        print("Creating warehouses...")
        warehouses = [
            Warehouse(
                name="Central Distribution", location_code="CD-01", is_active=True
            ),
            Warehouse(name="North West Hub", location_code="NW-02", is_active=True),
            Warehouse(name="South East Hub", location_code="SE-03", is_active=True),
        ]
        for w in warehouses:
            await warehouse_repo.save(w)

        print("Creating items...")
        items = []
        categories = ["Electronics", "Clothing", "Food", "Furniture"]
        for i in range(1, 21):
            item = Item(
                sku=SKU(value=f"ITEM-{i:05d}"),
                description=f"{random.choice(categories)} Product {i}",
                is_active=True,
            )
            await item_repo.save(item)
            items.append(item)

        print("Creating movements and generating anomalies...")
        now = datetime.now(UTC)
        total_anomalies = 0

        for item in items:
            warehouse = random.choice(warehouses)

            for days_ago in range(30, 0, -2):
                qty = Decimal(random.randint(10, 50))
                mov_type = random.choice(list(MovementType))
                mov_date = now - timedelta(days=days_ago)

                movement = Movement(
                    item_id=item.id,
                    warehouse_id=warehouse.id,
                    quantity=Quantity(value=qty),
                    movement_type=mov_type,
                    occurred_at=mov_date,
                )
                await movement_repo.save(movement)

            if random.random() < 0.3:
                qty = Decimal(random.randint(1000, 5000))
                mov_type = MovementType.OUT

                movement = Movement(
                    item_id=item.id,
                    warehouse_id=warehouse.id,
                    quantity=Quantity(value=qty),
                    movement_type=mov_type,
                    occurred_at=now,
                )
                await movement_repo.save(movement)

                event = MovementCreatedEvent(
                    movement_id=movement.id,
                    item_id=movement.item_id,
                    warehouse_id=movement.warehouse_id,
                    quantity_value=str(qty),
                    movement_type=mov_type,
                    occurrence_date=now,
                )

                severity, score = analysis_service.analyze(event)
                if severity and score:
                    anomaly = Anomaly(
                        movement_id=event.movement_id,
                        severity=severity,
                        score=score,
                        item_id=event.item_id,
                        detected_at=now,
                    )
                    await anomaly_repo.save(anomaly)
                    total_anomalies += 1

        await session.commit()

    print(
        f"Seed complete! Generated {len(items)} items, {len(warehouses)} warehouses, and {total_anomalies} anomalies."
    )


if __name__ == "__main__":
    asyncio.run(seed_data())
