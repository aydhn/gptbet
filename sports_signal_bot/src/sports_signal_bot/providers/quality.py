from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sports_signal_bot.providers.responses import ProviderQualityRecord


class ProviderQualityScorer:
    def __init__(self, thresholds: Dict[str, float] = None):
        self.thresholds = thresholds or {"overall": 0.5, "freshness": 0.3}

    def score_payload(
        self, raw_payload: Any, data_family: str, fetch_time: datetime
    ) -> ProviderQualityRecord:
        freshness = self.compute_freshness_score(fetch_time, fetch_time)  # simplified
        completeness = self.compute_completeness_score(raw_payload)
        consistency = self.compute_consistency_score(raw_payload)
        schema_validity = self.compute_schema_validity_score(raw_payload)

        overall, components = self.combine_provider_quality_scores(
            freshness, completeness, consistency, schema_validity
        )

        is_acceptable = overall >= self.thresholds.get(
            "overall", 0.5
        ) and freshness >= self.thresholds.get("freshness", 0.3)

        return ProviderQualityRecord(
            freshness_score=freshness,
            completeness_score=completeness,
            consistency_score=consistency,
            schema_validity_score=schema_validity,
            overall_score=overall,
            components=components,
            is_acceptable=is_acceptable,
        )

    def compute_freshness_score(
        self, snapshot_time: datetime, current_time: datetime
    ) -> float:
        if not snapshot_time or not current_time:
            return 0.0
        delta = (current_time - snapshot_time).total_seconds()
        # decay function example
        if delta < 3600:
            return 1.0
        elif delta < 86400:
            return 0.8
        else:
            return 0.5

    def compute_completeness_score(self, raw_payload: Any) -> float:
        if not raw_payload:
            return 0.0
        if isinstance(raw_payload, list) and len(raw_payload) > 0:
            return 1.0
        elif isinstance(raw_payload, dict) and len(raw_payload) > 0:
            return 1.0
        return 0.1

    def compute_consistency_score(self, raw_payload: Any) -> float:
        return 1.0  # placeholder

    def compute_schema_validity_score(self, raw_payload: Any) -> float:
        if raw_payload is None:
            return 0.0
        return 1.0  # placeholder

    def combine_provider_quality_scores(
        self,
        freshness: float,
        completeness: float,
        consistency: float,
        schema_validity: float,
    ):
        components = {
            "freshness": freshness,
            "completeness": completeness,
            "consistency": consistency,
            "schema_validity": schema_validity,
        }
        overall = (
            (freshness * 0.4)
            + (completeness * 0.3)
            + (schema_validity * 0.2)
            + (consistency * 0.1)
        )
        return overall, components

    def explain_provider_quality(self, record: ProviderQualityRecord) -> str:
        return f"Quality: {record.overall_score:.2f} (Acceptable: {record.is_acceptable}) - Components: {record.components}"
