from typing import Dict, Any, List
from .contracts import MetaTrainingDataset, MetaPredictionRecord, SourceCoverageRecord, MetaFeatureManifest
from .factory import StackerFactory

class StackerRunner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get("model_name", "identity")
        self.stacker = StackerFactory.create(self.model_name, self.config)

    def train(self, dataset: MetaTrainingDataset) -> Dict[str, Any]:
        """Train the stacker and return summary."""
        result = self.stacker.fit(dataset)

        # Build coverage
        coverage = self._build_coverage_report(dataset)

        manifest = MetaFeatureManifest(
            sport=dataset.sport,
            market_type=dataset.market_type,
            class_labels=dataset.class_labels,
            source_coverage=coverage,
            feature_columns=dataset.feature_names,
            total_records=len(dataset.records),
            missing_source_strategy=self.config.get("missing_source_strategy", "mean_impute")
        )

        result['manifest'] = manifest.model_dump()
        return result

    def predict(self, dataset: MetaTrainingDataset) -> List[MetaPredictionRecord]:
        """Predict using the trained stacker."""
        return self.stacker.predict(dataset)

    def _build_coverage_report(self, dataset: MetaTrainingDataset) -> List[SourceCoverageRecord]:
        source_counts = {}
        for r in dataset.records:
            for s in r.available_sources:
                source_counts[s] = source_counts.get(s, 0) + 1

        total_events = len(dataset.records)
        coverage_list = []
        for src, count in source_counts.items():
            coverage_list.append(SourceCoverageRecord(
                source_name=src,
                total_events=total_events,
                oof_events=count, # Assuming dataset is OOF
                oof_coverage_ratio=count / max(1, total_events),
                calibrated_ratio=1.0, # Handled by dataset builder
                excluded_rows=total_events - count
            ))
        return coverage_list
