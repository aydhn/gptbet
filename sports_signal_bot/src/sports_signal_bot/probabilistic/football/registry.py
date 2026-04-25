from typing import Dict, Type

from sports_signal_bot.probabilistic.football.model import FootballPoissonModel


class FootballModelRegistry:
    """Registry for probabilistic football models."""

    def __init__(self):
        self._models: Dict[str, Type] = {
            "football_poisson_baseline": FootballPoissonModel
            # Future models like dixon_coles will be registered here
        }

    def get_model(self, name: str):
        if name not in self._models:
            raise ValueError(f"Model {name} not found in registry.")
        return self._models[name]()


FOOTBALL_MODEL_REGISTRY = FootballModelRegistry()
