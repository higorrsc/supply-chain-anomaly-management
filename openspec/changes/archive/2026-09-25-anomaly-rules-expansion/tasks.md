# Tasks

## 1. Configuration & Schemas

- [x] 1.1 Update `anomaly_rules.yaml` to include the new structure with `deviation`, `business_hours`, and `max_quantity` rules with their respective toggles. Verify the file format is valid YAML.
- [x] 1.2 Update the Pydantic configuration models in `src/anomaly/infrastructure/config/settings.py` to parse the new nested rule structures. Verify parsing succeeds when the application loads the new YAML.
- [x] 1.3 Add domain configuration tests in `tests/anomaly/infrastructure/config/test_loader.py` to assert the new models parse correctly and fail cleanly on malformed data. Verify tests pass.

## 2. Rule Evaluator Abstractions

- [x] 2.1 Extract a new `RuleEvaluator` interface or protocol in `src/anomaly/domain/services/evaluators/` that takes a movement and context, returning a severity/score or `None`. Verify MyPy type checks pass.
- [x] 2.2 Refactor the existing standard deviation logic out of `AnomalyDetectionService` into a concrete `DeviationEvaluator`. Verify existing anomaly tests still pass.

## 3. New Rule Implementations

- [x] 3.1 Implement `BusinessHoursEvaluator` ensuring it compares movement times (UTC assumed) against configured start and end strings. Write domain unit tests for this evaluator and verify they pass.
- [x] 3.2 Implement `MaxQuantityEvaluator` checking `IN` vs `OUT` limits based on the movement type. Write domain unit tests for this evaluator and verify they pass.

## 4. Anomaly Service Integration

- [x] 4.1 Update `AnomalyDetectionService` to iterate through all enabled evaluators based on the configuration context.
- [x] 4.2 Implement severity aggregation logic in the service (e.g., returning the highest severity produced by the evaluators). Verify integration logic via unit tests.
- [x] 4.3 Run `make check` to ensure the entire E2E flow respects the new rules and all previous integration tests succeed.
