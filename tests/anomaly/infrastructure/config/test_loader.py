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
deviation_thresholds:
  low: 1.0
  high: 2.0
  critical: 3.0
""")

    rules = load_anomaly_rules(str(config_file))
    assert rules.enabled is True
    assert rules.deviation_thresholds.low == 1.0


def test_load_invalid_anomaly_rules(tmp_path: Path) -> None:
    config_file = tmp_path / "anomaly_rules.yaml"
    config_file.write_text("invalid_yaml: [")

    with pytest.raises(ConfigurationError):
        load_anomaly_rules(str(config_file))


def test_load_missing_file() -> None:
    with pytest.raises(ConfigurationError):
        load_anomaly_rules("non_existent_file.yaml")
