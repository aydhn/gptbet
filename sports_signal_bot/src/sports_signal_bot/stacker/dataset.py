from collections import defaultdict
from typing import Any, Dict, List, Optional

import numpy as np

from sports_signal_bot.ensemble.contracts import StandardizedPredictionRecord

from .contracts import MetaFeatureRecord, MetaTrainingDataset


class MetaDatasetBuilder:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled_sources = config.get("enabled_sources", [])
        self.use_only_calibrated = config.get("use_only_calibrated_sources", True)
        self.include_source_metadata = config.get("include_source_metadata", True)
        self.include_disagreement_features = config.get(
            "include_disagreement_features", True
        )
        self.missing_source_strategy = config.get(
            "missing_source_strategy", "mean_impute"
        )

    def build_meta_dataset(
        self,
        predictions: List[StandardizedPredictionRecord],
        target_labels: Dict[str, str],  # event_id -> label_name
        class_labels: List[str],
        sport: str,
        market_type: str,
        eligible_sources: Optional[List[str]] = None,
    ) -> MetaTrainingDataset:

        # 1. Group predictions by event
        event_preds = defaultdict(list)
        for p in predictions:
            if p.sport != sport or p.market_type != market_type:
                continue
            if self.use_only_calibrated and not p.is_calibrated:
                continue
            if self.enabled_sources and p.source_name not in self.enabled_sources:
                continue
            if eligible_sources is not None and p.source_name not in eligible_sources:
                continue

            event_preds[p.event_id].append(p)

        # 2. Build records
        records = []
        feature_names_set = set()

        for event_id, preds in event_preds.items():
            if not preds:
                continue

            target_name = target_labels.get(event_id)
            if not target_name and "inference" not in self.config:
                # We need targets for training
                continue

            target_idx = None
            if target_name in class_labels:
                target_idx = class_labels.index(target_name)

            record = self._build_single_record(
                event_id, sport, market_type, preds, class_labels
            )
            record.target_class_name = target_name
            record.target_class_index = target_idx

            # Record feature names
            feature_names_set.update(record.source_probabilities.keys())
            feature_names_set.update(record.confidence_features.keys())
            feature_names_set.update(record.agreement_features.keys())

            records.append(record)

        return MetaTrainingDataset(
            records=records,
            class_labels=class_labels,
            sport=sport,
            market_type=market_type,
            feature_names=sorted(list(feature_names_set)),
        )

    def _build_single_record(
        self,
        event_id: str,
        sport: str,
        market_type: str,
        preds: List[StandardizedPredictionRecord],
        class_labels: List[str],
    ) -> MetaFeatureRecord:

        prob_features = {}
        conf_features = {}
        avail_sources = []

        for p in preds:
            avail_sources.append(p.source_name)
            # Source probabilities
            for cls in class_labels:
                prob_val = p.probabilities.get(cls, 0.0)
                prob_features[f"{p.source_name}_prob_{cls}"] = prob_val

            # Confidence features
            probs = list(p.probabilities.values())
            if probs:
                max_prob = max(probs)
                conf_features[f"{p.source_name}_max_prob"] = max_prob
                entropy = -sum(p * np.log(p + 1e-9) for p in probs if p > 0)
                conf_features[f"{p.source_name}_entropy"] = entropy

        # Agreement features
        agreement_features = {}
        if self.include_disagreement_features and len(preds) > 1:
            for cls in class_labels:
                cls_probs = [p.probabilities.get(cls, 0.0) for p in preds]
                agreement_features[f"std_prob_{cls}"] = (
                    np.std(cls_probs) if cls_probs else 0.0
                )

        missing_sources = []
        if self.enabled_sources:
            missing_sources = [
                s for s in self.enabled_sources if s not in avail_sources
            ]

        context_features = {
            "source_count": len(preds),
            "missing_source_count": len(missing_sources),
        }

        return MetaFeatureRecord(
            event_id=event_id,
            sport=sport,
            market_type=market_type,
            source_probabilities=prob_features,
            confidence_features=conf_features,
            agreement_features=agreement_features,
            context_features=context_features,
            available_sources=avail_sources,
            missing_sources=missing_sources,
        )
