from typing import Dict, Type
from sports_signal_bot.training.trainers.base import BaseTrainer

class TrainerRegistry:
    def __init__(self):
        self._trainers: Dict[str, Type[BaseTrainer]] = {}

    def register(self, name: str, trainer_class: Type[BaseTrainer]):
        self._trainers[name] = trainer_class

    def get(self, name: str) -> Type[BaseTrainer]:
        if name not in self._trainers:
            raise ValueError(f"Trainer '{name}' not found in registry.")
        return self._trainers[name]

    def list_trainers(self) -> list:
        return list(self._trainers.keys())

TRAINER_REGISTRY = TrainerRegistry()

# Register defaults
from sports_signal_bot.training.trainers.logistic_regression import LogisticRegressionTrainer
from sports_signal_bot.training.trainers.gradient_boosting import GradientBoostingTrainer
from sports_signal_bot.training.trainers.random_forest import RandomForestTrainer
from sports_signal_bot.training.trainers.dummy import DummyTrainer

TRAINER_REGISTRY.register("logistic_regression", LogisticRegressionTrainer)
TRAINER_REGISTRY.register("gradient_boosting", GradientBoostingTrainer)
TRAINER_REGISTRY.register("random_forest", RandomForestTrainer)
TRAINER_REGISTRY.register("dummy", DummyTrainer)
