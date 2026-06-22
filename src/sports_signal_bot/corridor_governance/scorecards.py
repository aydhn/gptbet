from typing import Dict

from sports_signal_bot.corridor_governance.contracts import (
    SovereignInteroperabilityScorecardInputRecord,
    SovereignInteroperabilityScorecardRecord,
)


def build_interoperability_scorecard(
    input_record: SovereignInteroperabilityScorecardInputRecord,
) -> SovereignInteroperabilityScorecardRecord:
    return SovereignInteroperabilityScorecardRecord(
        scorecard_id=input_record.scorecard_id,
        scored_scope=input_record.scored_scope,
        scored_corridor_refs=input_record.scored_corridor_refs,
        scored_treaty_refs=input_record.scored_treaty_refs,
        region_pair_ref=input_record.region_pair_ref,
        dimension_scores=input_record.dimension_scores,
        overall_score=input_record.overall_score,
        overall_band=input_record.overall_band,
        caveat_summary=input_record.caveat_summary,
        blocking_gaps=input_record.blocking_gaps,
        warnings=input_record.warnings,
    )


def compute_scorecard_dimensions(
    raw_data: Dict[str, float], weights: Dict[str, float]
) -> Dict[str, float]:
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
