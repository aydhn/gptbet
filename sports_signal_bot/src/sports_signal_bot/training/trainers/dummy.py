from sklearn.dummy import DummyClassifier
from sports_signal_bot.training.trainers.base import SklearnClassifierTrainer
from typing import Dict, Any

class DummyTrainer(SklearnClassifierTrainer):
    @property
    def name(self) -> str:
        return "dummy"

    def __init__(self, config: Dict[str, Any]):
        # No scaling needed
        config.setdefault('scale_numeric', False)
        super().__init__(config)

        kwargs = self.config.get("model_kwargs", {})
        kwargs.setdefault("strategy", "prior")

        self.model = DummyClassifier(**kwargs)
