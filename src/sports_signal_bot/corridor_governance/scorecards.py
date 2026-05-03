from typing import List, Dict, Optional
from sports_signal_bot.corridor_governance.contracts import (
    SovereignInteroperabilityScorecardRecord,
    ScorecardDimensionRecord
)

def build_interoperability_scorecard(
    scorecard_id: str,
    scored_scope: str,
    scored_corridor_refs: List[str],
    scored_treaty_refs: List[str],
    region_pair_ref: str,
    dimension_scores: Dict[str, float],
    overall_score: float,
    overall_band: str,
    caveat_summary: List[str],
    blocking_gaps: List[str],
    warnings: List[str]
) -> SovereignInteroperabilityScorecardRecord:
    return SovereignInteroperabilityScorecardRecord(
        scorecard_id=scorecard_id,
        scored_scope=scored_scope,
        scored_corridor_refs=scored_corridor_refs,
        scored_treaty_refs=scored_treaty_refs,
        region_pair_ref=region_pair_ref,
        dimension_scores=dimension_scores,
        overall_score=overall_score,
        overall_band=overall_band,
        caveat_summary=caveat_summary,
        blocking_gaps=blocking_gaps,
        warnings=warnings
    )

def compute_scorecard_dimensions(raw_data: Dict[str, float], weights: Dict[str, float]) -> Dict[str, float]:
    computed = {}
    for dim, val in raw_data.items():
        weight = weights.get(dim, 1.0)
        computed[dim] = val * weight
    return computed

def map_score_to_band(score: float) -> str:
    if score >= 90:
        return "high_confidence_interop"
    elif score >= 75:
        return "strong"
    elif score >= 60:
        return "workable"
    elif score >= 40:
        return "guarded"
    elif score >= 20:
        return "weak"
    else:
        return "very_weak"
