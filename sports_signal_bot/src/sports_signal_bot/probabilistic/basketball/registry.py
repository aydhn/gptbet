from typing import Dict, Type
from sports_signal_bot.probabilistic.basketball.model import BasketballProbabilisticModel

class BasketballModelRegistry:
    """Registry for probabilistic basketball models."""
    def __init__(self):
        self._models: Dict[str, Type] = {
            "basketball_normal_baseline": BasketballProbabilisticModel
        }

    def get_model(self, name: str, config=None):
        if name not in self._models:
            raise ValueError(f"Model {name} not found in registry.")
        if config:
            return self._models[name](config)
        return self._models[name]()

BASKETBALL_MODEL_REGISTRY = BasketballModelRegistry()
