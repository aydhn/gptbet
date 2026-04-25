from typing import Any, Dict

from sports_signal_bot.training.registry import TRAINER_REGISTRY
from sports_signal_bot.training.trainers.base import BaseTrainer


class TrainerFactory:
    @staticmethod
    def create(name: str, config: Dict[str, Any]) -> BaseTrainer:
        trainer_class = TRAINER_REGISTRY.get(name)
        return trainer_class(config)
