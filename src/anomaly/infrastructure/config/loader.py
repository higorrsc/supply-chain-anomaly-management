from pathlib import Path

import yaml

from src.anomaly.domain.rules import AnomalyRules


class ConfigurationError(Exception):
    pass


def load_anomaly_rules(path: str = "anomaly_rules.yaml") -> AnomalyRules:
    file_path = Path(path)
    if not file_path.exists():
        raise ConfigurationError(f"Configuration file {path} not found.")

    with open(file_path) as f:
        try:
            data = yaml.safe_load(f)
            return AnomalyRules.model_validate(data)
        except Exception as e:
            raise ConfigurationError(f"Failed to parse configuration: {e}") from e
