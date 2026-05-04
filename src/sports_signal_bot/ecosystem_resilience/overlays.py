from typing import List, Dict
from sports_signal_bot.ecosystem_resilience.contracts import (
    FederationTrustOverlayRecord,
    TrustOverlayBand,
    TrustOverlayPenaltyRecord
)

def build_federation_trust_overlay(
    overlay_id: str,
    overlay_family: str,
    target_scope_ref: str,
    source_registry_refs: List[str],
    source_hub_refs: List[str],
    dimension_scores: Dict[str, float],
    sovereignty_deny: bool = False,
    is_stale: bool = False
) -> FederationTrustOverlayRecord:
    penalties = []
    if sovereignty_deny:
        penalties.append(TrustOverlayPenaltyRecord(penalty_id="pen-1", reason="sovereignty_deny", amount=1.0))
    if is_stale:
        penalties.append(TrustOverlayPenaltyRecord(penalty_id="pen-2", reason="stale_source", amount=0.5))

    final_score = compute_overlay_score(dimension_scores, penalties)
    band = compute_overlay_band(final_score, sovereignty_deny, is_stale)

    return FederationTrustOverlayRecord(
        overlay_id=overlay_id,
        overlay_family=overlay_family,
        target_scope_ref=target_scope_ref,
        source_registry_refs=source_registry_refs,
        source_hub_refs=source_hub_refs,
        dimension_scores=dimension_scores,
        penalties=penalties,
        final_overlay_band=band,
        final_overlay_score=final_score,
        caveat_refs=[],
        currentness_refs=[],
        warnings=[]
    )

def compute_overlay_score(dimension_scores: Dict[str, float], penalties: List[TrustOverlayPenaltyRecord]) -> float:
    if not dimension_scores:
        return 0.0
    base = sum(dimension_scores.values()) / len(dimension_scores)
    total_penalty = sum(p.amount for p in penalties)
    return max(0.0, base - total_penalty)

def compute_overlay_band(score: float, sovereignty_deny: bool, is_stale: bool) -> TrustOverlayBand:
    if sovereignty_deny:
        return TrustOverlayBand.HIGHLY_FRAGILE
    if is_stale and score > 0.4:
        return TrustOverlayBand.FRAGILE
    if score >= 0.8:
        return TrustOverlayBand.STRONG_BOUNDED_SIGNAL
    elif score >= 0.6:
        return TrustOverlayBand.BOUNDED_RELIABLE
    elif score >= 0.4:
        return TrustOverlayBand.RELIABLE_WITH_CAVEATS
    elif score >= 0.2:
        return TrustOverlayBand.CAVEATED
    elif score >= 0.1:
        return TrustOverlayBand.FRAGILE
    return TrustOverlayBand.HIGHLY_FRAGILE

def normalize_overlay_dimensions(raw_scores: Dict[str, float]) -> Dict[str, float]:
    return {k: min(1.0, max(0.0, v)) for k, v in raw_scores.items()}

def apply_overlay_penalties(score: float, penalties: List[TrustOverlayPenaltyRecord]) -> float:
    return max(0.0, score - sum(p.amount for p in penalties))

def explain_overlay_score(overlay: FederationTrustOverlayRecord) -> str:
    explanation = f"Base dims: {overlay.dimension_scores}. "
    if overlay.penalties:
        explanation += f"Penalties: {[p.reason for p in overlay.penalties]}. "
    explanation += f"Final score: {overlay.final_overlay_score} -> {overlay.final_overlay_band.value}."
    return explanation
