from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import TrustOverlayPenaltyRecord, FederationTrustOverlayRecord

def inject_sovereignty_penalties_into_overlay(overlay: FederationTrustOverlayRecord, sovereignty_deny: bool) -> FederationTrustOverlayRecord:
    if sovereignty_deny:
        overlay.penalties.append(TrustOverlayPenaltyRecord(
            penalty_id="sov-deny-pen",
            reason="Sovereignty policy denies this projection.",
            amount=1.0
        ))
        overlay.final_overlay_score = max(0.0, overlay.final_overlay_score - 1.0)
        overlay.final_overlay_band = "highly_fragile" # forces to lowest band
        overlay.warnings.append("Sovereignty denial masked by overlay.")
    return overlay

def prevent_overlay_from_masking_denials(overlay: FederationTrustOverlayRecord) -> bool:
    # Returns true if overlay successfully unmasked denials
    return any("sovereignty_deny" in p.reason for p in overlay.penalties)

def explain_quality_vs_allowability(overlay: FederationTrustOverlayRecord) -> str:
    quality_score = sum(overlay.dimension_scores.values()) / max(1, len(overlay.dimension_scores))
    allowability = "Denied" if any("sovereignty" in p.reason.lower() for p in overlay.penalties) else "Allowed"
    return f"Quality: {quality_score:.2f}, Allowability: {allowability}"
