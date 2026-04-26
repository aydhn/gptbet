from typing import List
from sports_signal_bot.portfolio.contracts import PortfolioCandidateRecord, PortfolioConfig, CorrelationPlaceholderRecord

def detect_related_market_candidates(candidate: PortfolioCandidateRecord, current_allocations: List[PortfolioCandidateRecord], config: PortfolioConfig) -> List[CorrelationPlaceholderRecord]:
    if not config.correlation_guard_enabled:
        return []

    guards = []
    for allocated in current_allocations:
        # Simplistic placeholder: if it's the exact same event_id but a different market
        if allocated.event_id == candidate.event_id and allocated.market_type != candidate.market_type:
            guards.append(CorrelationPlaceholderRecord(
                event_id_a=candidate.event_id,
                event_id_b=allocated.event_id,
                relation_type="same_event_different_market",
                correlation_risk_level="high",
                reason=f"Already allocated {allocated.market_type} for event {candidate.event_id}"
            ))

    return guards
