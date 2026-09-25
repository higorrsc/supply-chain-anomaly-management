# Tasks

## 1. Event Dispatcher Infrastructure

- [x] 1.1 Create `DomainEvent` and `EventDispatcher` abstractions in the core domain and verify they can be imported.
- [x] 1.2 Implement a simple in-memory `AsyncEventDispatcher` in the core infrastructure and verify it allows subscribing and publishing events successfully via unit tests.
- [x] 1.3 Create `MovementCreatedEvent` in the Inventory domain events and verify it holds the correct movement payload structure.

## 2. Inventory Context Adjustments

- [x] 2.1 Inject `EventDispatcher` into `CreateMovementUseCase` and verify the dependency injection setup is correct in FastAPI dependencies.
- [x] 2.2 Update `CreateMovementUseCase` to publish `MovementCreatedEvent` upon successful creation and verify this via a mocked dispatcher in the use case test.

## 3. Configuration & Rule Engine (Anomaly Context)

- [x] 3.1 Create `AnomalyRules` Pydantic models in the Anomaly domain/infrastructure to represent YAML structure and verify schema validation rules.
- [x] 3.2 Add `PyYAML` to the project dependencies (if not already present) and verify it installs correctly.
- [x] 3.3 Create a configuration loader that reads `anomaly_rules.yaml` into the Pydantic model on application startup and verify it fails gracefully on invalid files.
- [x] 3.4 Create a sample `anomaly_rules.yaml` in the project root containing default rules and verify it is discoverable by the loader.

## 4. Anomaly Detection Domain Service

- [x] 4.1 Create `MovementAnomalyAnalysisService` in the Anomaly domain and verify its signature accepts a movement and configuration rules.
- [x] 4.2 Implement the calculation logic inside the service (e.g., standard deviation bounds based on config) and verify edge cases via unit tests (high severity vs normal).

## 5. Event Handling & Orchestration

- [x] 5.1 Create `DetectAnomalyForMovementUseCase` (or event handler) in the Anomaly application layer that listens for `MovementCreatedEvent` and verify it correctly parses the event payload.
- [x] 5.2 Implement the handler logic: invoke `MovementAnomalyAnalysisService`, and if an anomaly is detected, persist it via `AnomalyRepository` and verify behavior via integration/use-case tests.
- [x] 5.3 Wire the handler to the `EventDispatcher` at application startup (in `main.py` lifespan) and verify the event flows from Inventory to Anomaly properly using an end-to-end test.
