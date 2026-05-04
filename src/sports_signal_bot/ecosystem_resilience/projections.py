from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import (
    BaselineMarketplaceSignalRecord,
    TrustOverlayBand
)

def project_signal_into_overlay_or_score(signal: BaselineMarketplaceSignalRecord, current_score: float) -> float:
    if signal.relevance_band == "suppressed_signal" or signal.relevance_band == "irrelevant":
        return current_score
    if signal.relevance_band == "weak_hint":
        return current_score + 0.05
    if signal.relevance_band == "bounded_hint":
        return current_score + 0.1
    if signal.relevance_band == "useful_signal":
        return current_score + 0.15
    if signal.relevance_band == "high_relevance_but_caveated":
        return current_score + 0.05
    return current_score

def project_marketplace_signals_into_scorecards(signals: List[BaselineMarketplaceSignalRecord], base_score: float) -> float:
    for s in signals:
        base_score = project_signal_into_overlay_or_score(s, base_score)
    return min(1.0, max(0.0, base_score))

def cap_scores_due_to_signal_staleness(score: float, is_stale: bool) -> float:
    return min(score, 0.4) if is_stale else score

def explain_signal_contribution_to_score(signals: List[BaselineMarketplaceSignalRecord]) -> str:
    contributions = []
    for s in signals:
        contributions.append(f"{s.signal_id}: {s.relevance_band}")
    return "Signal Contributions: " + ", ".join(contributions)
