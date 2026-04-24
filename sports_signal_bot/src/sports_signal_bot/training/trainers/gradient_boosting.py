from sklearn.ensemble import HistGradientBoostingClassifier
from sports_signal_bot.training.trainers.base import SklearnClassifierTrainer
from typing import Dict, Any

class GradientBoostingTrainer(SklearnClassifierTrainer):
    @property
    def name(self) -> str:
        return "gradient_boosting"

    def __init__(self, config: Dict[str, Any]):
        # Trees usually don't need scaling
        config.setdefault('scale_numeric', False)
        super().__init__(config)

        kwargs = self.config.get("model_kwargs", {})

        # Support class_weight configuration
        class_weight = self.config.get("class_weight")
        if class_weight:
            kwargs["class_weight"] = class_weight

        self.model = HistGradientBoostingClassifier(**kwargs)
