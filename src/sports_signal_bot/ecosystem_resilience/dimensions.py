from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import TrustOverlayDimensionRecord

def build_trust_overlay_dimension(
    dimension_id: str,
    dimension_family: str,
    raw_signal_refs: List[str],
    normalized_score: float,
    weighting_ref: str,
    freshness_state: str = "fresh",
    caveat_state: str = "none"
) -> TrustOverlayDimensionRecord:
    return TrustOverlayDimensionRecord(
        dimension_id=dimension_id,
        dimension_family=dimension_family,
        raw_signal_refs=raw_signal_refs,
        normalized_score=max(0.0, min(1.0, normalized_score)),
        weighting_ref=weighting_ref,
        freshness_state=freshness_state,
        caveat_state=caveat_state,
        warnings=[]
    )
