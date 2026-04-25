from sklearn.linear_model import LogisticRegression
from typing import Dict, Any, List
from .base import BaseStacker
from ..contracts import MetaTrainingDataset

class MetaLogisticStacker(BaseStacker):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def fit(self, dataset: MetaTrainingDataset) -> Dict[str, Any]:
        self.sport = dataset.sport
        self.market_type = dataset.market_type
        self.class_labels = dataset.class_labels
        self.feature_names = dataset.feature_names

        df = self._prepare_df(dataset, for_training=True)
        # Handle nan for training
        df.fillna(df.mean(), inplace=True)
        df.fillna(0.0, inplace=True)

        X = df[self.feature_names]
        y = df['target']

        # Hyperparameters
        params = self.config.get("meta_model_hyperparams", {})
        c_val = params.get("C", 1.0)
        max_iter = params.get("max_iter", 1000)

        # Determine multi_class based on the number of unique target classes
        num_classes = len(self.class_labels)
        if num_classes > 2:
            self.model = LogisticRegression(C=c_val, max_iter=max_iter) # multinomial is default if multiclass
        else:
            self.model = LogisticRegression(C=c_val, max_iter=max_iter)

        self.model.fit(X, y)
        self.is_fitted = True

        return {
            "status": "success",
            "model": "MetaLogisticStacker",
            "classes": self.class_labels,
            "feature_count": len(self.feature_names)
        }

    def predict_proba(self, dataset: MetaTrainingDataset) -> List[Dict[str, float]]:
        df = self._prepare_df(dataset, for_training=False)
        X = df[self.feature_names]

        probas = self.model.predict_proba(X)
        model_classes = self.model.classes_

        results = []
        for i in range(len(probas)):
            prob_dict = {}
            for cls_name in self.class_labels:
                cls_idx = self.class_labels.index(cls_name)
                if cls_idx in model_classes:
                    model_idx = list(model_classes).index(cls_idx)
                    prob_dict[cls_name] = float(probas[i][model_idx])
                else:
                    prob_dict[cls_name] = 0.0
            results.append(prob_dict)

        return results
