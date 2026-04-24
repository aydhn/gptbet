from sklearn.linear_model import LogisticRegression
from sports_signal_bot.training.trainers.base import SklearnClassifierTrainer
from typing import Dict, Any

class LogisticRegressionTrainer(SklearnClassifierTrainer):
    @property
    def name(self) -> str:
        return "logistic_regression"

    def __init__(self, config: Dict[str, Any]):
        # Default to scaling for Logistic Regression
        config.setdefault('scale_numeric', True)
        super().__init__(config)

        kwargs = self.config.get("model_kwargs", {})
        kwargs.setdefault("max_iter", 1000)

        # Support class_weight configuration
        class_weight = self.config.get("class_weight")
        if class_weight:
            kwargs["class_weight"] = class_weight

        self.model = LogisticRegression(**kwargs)
