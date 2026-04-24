from typing import Dict, Any
from sports_signal_bot.training.trainers.base import BaseTrainer
from sports_signal_bot.training.registry import TRAINER_REGISTRY

class TrainerFactory:
    @staticmethod
    def create(name: str, config: Dict[str, Any]) -> BaseTrainer:
        trainer_class = TRAINER_REGISTRY.get(name)
        return trainer_class(config)
