from typing import Dict, Any, List
from .contracts import ThresholdCandidateRecord, ThresholdFrontierRecord

class ThresholdFrontierBuilder:
    def __init__(self, candidates: List[ThresholdCandidateRecord], sport: str, market_type: str):
        self.candidates = sorted(candidates, key=lambda c: c.score_threshold)
        self.sport = sport
        self.market_type = market_type

    def build(self) -> ThresholdFrontierRecord:
        curve = []
        for c in self.candidates:
            pt = {
                "score_threshold": c.score_threshold,
                "coverage_rate": c.coverage_rate,
                "accepted_count": float(c.accepted_count),
                "objective_value": c.objective_value
            }
            if c.edge_threshold is not None:
                pt["edge_threshold"] = c.edge_threshold

            for k, v in c.quality_metrics.items():
                pt[k] = v

            curve.append(pt)

        return ThresholdFrontierRecord(
            sport=self.sport,
            market_type=self.market_type,
            tradeoff_curve=curve
        )

    def summarize_tradeoff_curve(self, record: ThresholdFrontierRecord) -> Dict[str, Any]:
        if not record.tradeoff_curve:
            return {}

        max_cov = max(pt["coverage_rate"] for pt in record.tradeoff_curve)
        max_obj = max(pt["objective_value"] for pt in record.tradeoff_curve)

        return {
            "max_coverage": max_cov,
            "max_objective": max_obj,
            "num_points": len(record.tradeoff_curve)
        }
