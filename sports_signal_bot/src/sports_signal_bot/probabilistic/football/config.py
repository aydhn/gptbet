from typing import Any, Dict

from sports_signal_bot.probabilistic.football.contracts import \
    GoalEnvironmentConfig


def load_football_probabilistic_config(
    overrides: Dict[str, Any] = None,
) -> GoalEnvironmentConfig:
    """Loads and optionally overrides default goal environment configuration."""
    config = GoalEnvironmentConfig()
    if overrides:
        for k, v in overrides.items():
            if hasattr(config, k):
                setattr(config, k, v)
    return config
