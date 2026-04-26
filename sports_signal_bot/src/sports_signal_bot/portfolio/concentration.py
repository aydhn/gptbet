from typing import List, Dict
from sports_signal_bot.portfolio.contracts import PortfolioCandidateRecord, PortfolioConfig, ConcentrationRecord

def compute_concentration_risk(candidate: PortfolioCandidateRecord, current_allocations: List[PortfolioCandidateRecord], config: PortfolioConfig) -> ConcentrationRecord:
    # Placeholder implementation
    sport_count = sum(1 for c in current_allocations if c.sport == candidate.sport)
    market_count = sum(1 for c in current_allocations if c.market_type == candidate.market_type)

    # Simple penalty: 1% per existing allocation in same sport/market
    sport_conc = sport_count * 0.01
    market_conc = market_count * 0.01
    source_conc = 0.0 # Placeholder

    total_penalty = (
        sport_conc * config.concentration_penalty_weights.get("sport", 0.1) +
        market_conc * config.concentration_penalty_weights.get("market", 0.1) +
        source_conc * config.concentration_penalty_weights.get("source", 0.05)
    )

    return ConcentrationRecord(
        sport_concentration=sport_conc,
        market_concentration=market_conc,
        source_concentration=source_conc,
        overall_penalty=min(0.5, total_penalty) # Cap penalty at 50%
    )
