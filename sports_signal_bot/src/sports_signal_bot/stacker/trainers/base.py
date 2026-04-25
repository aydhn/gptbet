from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from sports_signal_bot.ensemble.contracts import StandardizedPredictionRecord

from ..contracts import (MetaPredictionDiagnostics, MetaPredictionRecord,
                         MetaTrainingDataset)


class BaseStacker(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.feature_names = []
        self.class_labels = []
        self.sport = ""
        self.market_type = ""
        self.is_fitted = False

    @abstractmethod
    def fit(self, dataset: MetaTrainingDataset) -> Dict[str, Any]:
        """Fit the stacker model"""
        pass

    @abstractmethod
    def predict_proba(self, dataset: MetaTrainingDataset) -> List[Dict[str, float]]:
        """Predict probabilities"""
        pass

    def _prepare_df(
        self, dataset: MetaTrainingDataset, for_training: bool = False
    ) -> pd.DataFrame:
        rows = []
        for r in dataset.records:
            row = {}
            row.update(r.source_probabilities)
            row.update(r.confidence_features)
            row.update(r.agreement_features)
            row.update(r.metadata_features)
            row.update(r.context_features)
            if for_training:
                row["target"] = r.target_class_index
            rows.append(row)

        df = pd.DataFrame(rows)
        # Handle missing columns and ordering based on feature_names
        if self.is_fitted and not for_training:
            for f in self.feature_names:
                if f not in df.columns:
                    df[f] = 0.0  # simple impute or NaN depending on model
            df = df[self.feature_names]
            # mean imputation
            df.fillna(df.mean(), inplace=True)
            df.fillna(0.0, inplace=True)

        return df

    def predict(self, dataset: MetaTrainingDataset) -> List[MetaPredictionRecord]:
        if not self.is_fitted:
            raise ValueError("Stacker must be fitted before prediction.")

        probas_list = self.predict_proba(dataset)
        records = []

        for i, record in enumerate(dataset.records):
            probas = probas_list[i]
            predicted_class = max(probas.items(), key=lambda k: k[1])[0]

            # Diagnostics
            sorted_probs = sorted(probas.values(), reverse=True)
            margin = (
                sorted_probs[0] - sorted_probs[1]
                if len(sorted_probs) > 1
                else sorted_probs[0]
            )
            confidence = sorted_probs[0]

            diagnostics = MetaPredictionDiagnostics(
                sources_used=len(record.available_sources),
                missing_sources=len(record.missing_sources),
                fallback_used=False,
                meta_confidence=confidence,
                top_class_margin=margin,
            )

            pred_record = MetaPredictionRecord(
                event_id=record.event_id,
                sport=self.sport,
                market_type=self.market_type,
                stacker_name=self.__class__.__name__,
                final_probabilities=probas,
                predicted_class=predicted_class,
                diagnostics=diagnostics,
            )
            records.append(pred_record)

        return records
