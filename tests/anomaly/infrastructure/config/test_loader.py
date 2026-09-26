from pathlib import Path

import pytest

from src.anomaly.infrastructure.config.loader import (
    ConfigurationError,
    load_anomaly_rules,
)


def test_load_valid_anomaly_rules(tmp_path: Path) -> None:
    config_file = tmp_path / "anomaly_rules.yaml"
    config_file.write_text("""
enabled: true
rules:
  deviation:
    enabled: true
    thresholds:
      low: 1.0
      high: 2.0
      critical: 3.0
  business_hours:
    enabled: true
    start_time: "08:00"
    end_time: "18:00"
  max_quantity:
    enabled: true
    max_in: 100
    max_out: 50
""")

    rules = load_anomaly_rules(str(config_file))
    assert rules.enabled is True
    assert rules.rules.deviation.thresholds.low == 1.0
    assert rules.rules.business_hours.enabled is True
    assert rules.rules.max_quantity.max_in == 100


def test_load_invalid_anomaly_rules(tmp_path: Path) -> None:
    config_file = tmp_path / "anomaly_rules.yaml"
    config_file.write_text("invalid_yaml: [")

    with pytest.raises(ConfigurationError):
        load_anomaly_rules(str(config_file))


def test_load_missing_file() -> None:
    with pytest.raises(ConfigurationError):
        load_anomaly_rules("non_existent_file.yaml")
