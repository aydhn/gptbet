from typing import Any, Dict, List

from ..contracts import MetaTrainingDataset
from .base import BaseStacker


class MetaIdentityStacker(BaseStacker):
    """
    Identity/Fallback Stacker.
    Simply averages the probabilities of available calibrated sources,
    or just returns the first source if no others exist.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.is_fitted = True  # Doesn't require fitting

    def fit(self, dataset: MetaTrainingDataset) -> Dict[str, Any]:
        self.sport = dataset.sport
        self.market_type = dataset.market_type
        self.class_labels = dataset.class_labels
        self.feature_names = dataset.feature_names

        return {
            "status": "success",
            "model": "MetaIdentityStacker",
            "classes": self.class_labels,
            "feature_count": len(self.feature_names),
        }

    def predict_proba(self, dataset: MetaTrainingDataset) -> List[Dict[str, float]]:
        results = []
        for record in dataset.records:
            prob_dict = {}
            source_count = 0

            # Simple average of available source probabilities
            for cls in self.class_labels:
                prob_dict[cls] = 0.0

            for source in record.available_sources:
                source_count += 1
                for cls in self.class_labels:
                    prob_dict[cls] += record.source_probabilities.get(
                        f"{source}_prob_{cls}", 0.0
                    )

            if source_count > 0:
                for cls in self.class_labels:
                    prob_dict[cls] /= source_count

            # Handle edge case where no sources are available
            if sum(prob_dict.values()) == 0.0 and len(self.class_labels) > 0:
                uniform_prob = 1.0 / len(self.class_labels)
                for cls in self.class_labels:
                    prob_dict[cls] = uniform_prob

            results.append(prob_dict)

        return results
